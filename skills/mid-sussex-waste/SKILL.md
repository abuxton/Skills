---
name: mid-sussex-waste
description: 'Retrieve live Mid Sussex waste collection dates from the public Whitespace site using Playwright-driven browser automation, then return the next collection plus current and next month schedules.'
---

# Mid Sussex Waste Collection Schedule Finder

Retrieve live bin collection dates from the Mid Sussex Whitespace waste site by following the real browser flow, resolving the correct address, and returning a structured schedule summary. Treat the live schedule page as the only source of truth.

## Role

You are an expert web automation specialist focused on safe, browser-driven data extraction from dynamic sites.

- Use Playwright-driven browser automation as the primary mechanism
- Discover the live waste-service route from the start page instead of guessing URLs
- Ask the user for address details only when the live flow reaches the address lookup form
- Stop and report failures or ambiguity plainly instead of inventing data

## Workflow

1. **Start from the live entry point** — Open `https://sms-wrp.whitespacews.com/#!` and inspect the real links, buttons, and forms that lead into the waste collection journey. Do not jump directly to guessed or stale URLs.

2. **Discover the live route** — Follow the waste-service flow until the site produces a live `Track`-style route or equivalent session-backed navigation state. Treat values such as `Track`, `seq`, `pIndex`, or other request parameters as run-specific and discover them from the active session only.

3. **Collect address details at the point of need** — When the address form is actually present, ask the user for exactly these fields:
   - house number or house name
   - street
   - postcode

4. **Submit the lookup and resolve the address** — Fill and submit the live address form. If the site returns multiple matching addresses, show the options clearly and ask the user to confirm the exact address. Never guess past an ambiguous result.

5. **Open the schedule page and extract events** — Navigate to the selected address result and use the visible collection schedule area as the source of truth. Extract at minimum:
   - collection date as displayed by the site
   - service name

6. **Normalize and group the data** — Convert each collection date into machine-friendly ISO format while preserving the displayed date string. Group multiple services that share the same date into a single event entry.

7. **Filter to the required reporting window** — Using the current runtime date, return only:
   - the next upcoming collection from now
   - all collections in the current calendar month
   - all collections in the next calendar month
   If the current or next month has no events, state that explicitly.

8. **Return both required outputs** — Produce the result in this order:
   - a Markdown summary containing the selected address, the final schedule page URL, the next upcoming collection and services, the current-month schedule, and the next-month schedule
   - a JSON object with this shape:

   ```json
   {
     "selected_address": "67, DE LA WARR ROAD, EAST GRINSTEAD, EAST GRINSTEAD, WEST SUSSEX",
     "source_url": "https://sms-wrp.whitespacews.com/mop.php?...",
     "next_collection": {
       "date": "2026-04-16",
       "display_date": "16/04/2026",
       "services": [
         "Domestic Food Waste Service",
         "Domestic Recycling Waste Collection Service",
         "Domestic Refuse Waste Collection Service"
       ]
     },
     "collections": [
       {
         "month": "2026-04",
         "events": [
           {
             "date": "2026-04-16",
             "display_date": "16/04/2026",
             "services": [
               "Domestic Food Waste Service",
               "Domestic Recycling Waste Collection Service",
               "Domestic Refuse Waste Collection Service"
             ]
           }
         ]
       },
       {
         "month": "2026-05",
         "events": [
           {
             "date": "2026-05-07",
             "display_date": "07/05/2026",
             "services": [
               "Domestic Food Waste Service",
               "Domestic Refuse Waste Collection Service"
             ]
           }
         ]
       }
     ]
   }
   ```

   Populate the structure only with live data from the current run.

9. **Fail explicitly when the live flow cannot be verified** — Stop and explain the exact failure if any of these occur:
   - the waste-service entry point cannot be identified from the live start page
   - the dynamic tracking route cannot be discovered
   - the address form cannot be found
   - no address results match the submitted details
   - the schedule page loads but no collection data is present

## Notes

- Do not hard-code `Track`, `seq`, `pIndex`, or other session-like values from examples.
- Do not report sample data, guessed HTML, or stale schedule information as live results.
- Do not scrape outside the intended waste collection journey on `sms-wrp.whitespacews.com`.
- Prefer live DOM inspection and page interaction over brittle text guessing.
- Preserve the selected address and the actual final schedule page URL in the final answer.
