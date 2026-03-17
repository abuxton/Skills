---
description: Create a new skill for running GitHub Actions locally using nektos/act
globs: ["skills/**", "AGENTS.md"]
---

# Goal
Create a new agent skill (`skills/act/SKILL.md`) that enables agents to run, debug, and troubleshoot GitHub Actions locally using `nektos/act`.

# Persona
Act as a **DevOps & GitHub Actions Expert** specialized in local CI/CD pipelines and containerized workflows.

# Context
- **Project Standards**: Read `AGENTS.md` to understand the repository's skill structure, frontmatter requirements, and documentation standards.
- **Tool Documentation**: Fetch the latest documentation for `nektos/act` (https://nektosact.com/) to ensure the skill uses up-to-date commands and flags.

# Instructions

1. **Analyze Requirements**:
   - Read `AGENTS.md` to identify where to register the new skill.
   - Fetch the `nektos/act` homepage or usage guide to understand core commands (`act -l`, `act -j`, artifact handling).

2. **Scaffold the Skill**:
   - Create directory `skills/act/`.
   - Create `skills/act/SKILL.md` following the template in `AGENTS.md`.

3. **Define Skill Content**:
   - **Role**: Define the agent as an expert in local workflow execution.
   - **Workflow**:
     1. **Prerequisite Check**: Verify Docker is running and `act` is installed.
     2. **Workflow Validation**: Check `.github/workflows` for syntax errors before running.
     3. **Execution**: Run specific jobs or events (e.g., `act push`, `act -j test`).
     4. **Debugging**: Analyze failure logs, inspect artifacts, and suggest fixes.
   - **Notes**: Add tips for handling secrets (`.secrets` file), env vars, and large images.

4. **Register the Skill**:
   - Add `act` to the "Available Skills" table in `AGENTS.md`.
   - Add `act` to the "Available Skills" table in `README.md` (if present).

5. **Validation**:
   - Ensure the new `SKILL.md` uses the correct YAML frontmatter.
   - Verify the instructions are compatible with the current project structure.
