#!/usr/bin/env python3
"""
fetch_xkcd.py — Resolve XKCD comic requests and emit reusable output snippets.

Supported request forms:
    latest                      Fetch the latest comic via /info.0.json
    random                      Resolve a random comic via c.xkcd.com/random/comic/
    <numeric id>                Fetch a specific comic number
    https://xkcd.com/<id>/      Fetch a specific XKCD URL
    <search phrase>             Match against XKCD archive titles conservatively

Examples:
    python3 fetch_xkcd.py latest --format json --validate
    python3 fetch_xkcd.py random --format markdown-linked
    python3 fetch_xkcd.py "subduction ocean crust" --format html-anchor --validate
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser


ARCHIVE_URL = "https://xkcd.com/archive/"
LATEST_JSON_URL = "https://xkcd.com/info.0.json"
RANDOM_URL = "https://c.xkcd.com/random/comic/"
USER_AGENT = "xkcd-says-what/1.0 (+https://github.com/abuxton/Skills)"
COMIC_ID_RE = re.compile(r"^https?://xkcd\.com/(\d+)/?$")


@dataclass(frozen=True)
class Comic:
    num: int
    title: str
    alt: str
    image_url: str
    page_url: str


@dataclass(frozen=True)
class SearchCandidate:
    num: int
    title: str
    score: float


class ArchiveParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.entries: list[tuple[int, str]] = []
        self._current_num: int | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href")
        title = attr_map.get("title")
        if not href or not title:
            return
        match = re.match(r"^/(\d+)/$", href)
        if not match:
            return
        self._current_num = int(match.group(1))
        self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_num is not None:
            self._text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self._current_num is None:
            return
        title = html.unescape("".join(self._text_parts).strip())
        if title:
            self.entries.append((self._current_num, title))
        self._current_num = None
        self._text_parts = []


def fetch_text(url: str) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        body = response.read().decode("utf-8")
        return body, response.geturl()


def fetch_json(url: str) -> dict:
    body, _ = fetch_text(url)
    return json.loads(body)


def build_comic(payload: dict) -> Comic:
    num = int(payload["num"])
    page_url = f"https://xkcd.com/{num}/"
    return Comic(
        num=num,
        title=str(payload["title"]),
        alt=str(payload.get("alt", "")),
        image_url=str(payload["img"]),
        page_url=page_url,
    )


def fetch_latest() -> Comic:
    return build_comic(fetch_json(LATEST_JSON_URL))


def fetch_by_id(num: int) -> Comic:
    return build_comic(fetch_json(f"https://xkcd.com/{num}/info.0.json"))


def fetch_random() -> Comic:
    _, final_url = fetch_text(RANDOM_URL)
    match = COMIC_ID_RE.match(final_url)
    if not match:
        raise RuntimeError(f"Could not extract comic id from redirected URL: {final_url}")
    return fetch_by_id(int(match.group(1)))


def normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def archive_entries() -> list[tuple[int, str]]:
    archive_html, _ = fetch_text(ARCHIVE_URL)
    parser = ArchiveParser()
    parser.feed(archive_html)
    return parser.entries


def score_candidate(query: str, title: str) -> float:
    normalized_query = normalize(query)
    normalized_title = normalize(title)
    if not normalized_query or not normalized_title:
        return 0.0

    ratio = difflib.SequenceMatcher(None, normalized_query, normalized_title).ratio()
    query_tokens = set(normalized_query.split())
    title_tokens = set(normalized_title.split())
    overlap = len(query_tokens & title_tokens) / max(len(query_tokens), 1)
    substring_bonus = 0.15 if normalized_query in normalized_title or normalized_title in normalized_query else 0.0
    return ratio * 0.45 + overlap * 0.40 + substring_bonus


def search_archive(query: str, limit: int = 3) -> tuple[Comic, list[SearchCandidate]]:
    candidates = [
        SearchCandidate(num=num, title=title, score=score_candidate(query, title))
        for num, title in archive_entries()
    ]
    ranked = sorted(candidates, key=lambda candidate: (-candidate.score, -candidate.num))
    if not ranked:
        raise RuntimeError("Archive search returned no comics.")
    top = ranked[0]
    return fetch_by_id(top.num), ranked[:limit]


def parse_query(raw_query: str) -> tuple[str, str | int]:
    stripped = raw_query.strip()
    lowered = stripped.lower()
    if lowered == "latest":
        return "latest", stripped
    if lowered == "random":
        return "random", stripped
    if stripped.isdigit():
        return "id", int(stripped)
    url_match = COMIC_ID_RE.match(stripped)
    if url_match:
        return "id", int(url_match.group(1))
    return "search", stripped


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def build_snippets(comic: Comic) -> dict[str, str]:
    title = escape_attr(comic.title)
    alt = escape_attr(comic.alt)
    page_url = escape_attr(comic.page_url)
    image_url = escape_attr(comic.image_url)
    markdown_title = comic.title.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    markdown_alt = comic.alt.replace("\\", "\\\\").replace('"', '\\"')
    markdown_image = f'![{markdown_title}]({comic.image_url} "{markdown_alt}")'
    markdown_linked = f'[![{markdown_title}]({comic.image_url} "{markdown_alt}")]({comic.page_url})'
    html_anchor = f'<a href="{page_url}">{title}</a>'
    html_image = (
        f'<img src="{image_url}" alt="{title}" title="{alt}" />'
    )
    return {
        "markdown_image": markdown_image,
        "markdown_linked_image": markdown_linked,
        "html_anchor": html_anchor,
        "html_image": html_image,
    }


def validate_url(url: str) -> int:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return int(response.status)


def resolve(query: str) -> dict:
    mode, value = parse_query(query)
    search_candidates: list[SearchCandidate] = []

    if mode == "latest":
        comic = fetch_latest()
        rationale = "Resolved using the latest XKCD JSON feed."
    elif mode == "random":
        comic = fetch_random()
        rationale = "Resolved by following XKCD's random comic redirect."
    elif mode == "id":
        comic = fetch_by_id(int(value))
        rationale = f"Resolved directly from comic id {value}."
    else:
        comic, search_candidates = search_archive(str(value))
        best_score = search_candidates[0].score if search_candidates else 0.0
        rationale = (
            f"Resolved from archive title matching with top score {best_score:.3f}. "
            "Search is title-based and approximate."
        )

    snippets = build_snippets(comic)
    result = {
        "query": query,
        "resolved_mode": mode,
        "selection_reason": rationale,
        "comic": {
            "num": comic.num,
            "title": comic.title,
            "alt": comic.alt,
            "page_url": comic.page_url,
            "image_url": comic.image_url,
        },
        "snippets": snippets,
    }
    if search_candidates:
        result["candidates"] = [
            {"num": candidate.num, "title": candidate.title, "score": round(candidate.score, 3)}
            for candidate in search_candidates
        ]
    return result


def render(result: dict, output_format: str) -> str:
    snippets = result["snippets"]
    if output_format == "json":
        return json.dumps(result, indent=2)
    if output_format == "markdown":
        return snippets["markdown_image"]
    if output_format == "markdown-linked":
        return snippets["markdown_linked_image"]
    if output_format == "html-anchor":
        return snippets["html_anchor"]
    if output_format == "html-image":
        return snippets["html_image"]
    if output_format == "text":
        comic = result["comic"]
        return (
            f'#{comic["num"]} — {comic["title"]}\n'
            f'Page: {comic["page_url"]}\n'
            f'Image: {comic["image_url"]}\n'
            f'Reason: {result["selection_reason"]}'
        )
    raise ValueError(f"Unsupported format: {output_format}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="latest, random, numeric id, XKCD URL, or search phrase")
    parser.add_argument(
        "--format",
        default="json",
        choices=("json", "markdown", "markdown-linked", "html-anchor", "html-image", "text"),
        help="Output format to print.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the page and image URLs and include the HTTP status codes in JSON output.",
    )
    return parser.parse_args(argv[1:])


def main() -> None:
    args = parse_args(sys.argv)
    query = " ".join(args.query)

    try:
        result = resolve(query)
        if args.validate:
            page_url = result["comic"]["page_url"]
            image_url = result["comic"]["image_url"]
            result["validation"] = {
                "page_url": validate_url(page_url),
                "image_url": validate_url(image_url),
            }
        print(render(result, args.format))
    except urllib.error.HTTPError as error:
        print(
            f"ERROR: request failed with HTTP {error.code} for {error.url}",
            file=sys.stderr,
        )
        sys.exit(1)
    except urllib.error.URLError as error:
        print(f"ERROR: network request failed: {error.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
