---
name: "hoi4-modding"
description: "Use when the user wants to create, refactor, debug, or review Hearts of Iron IV mods, including focus trees, events, decisions, ideas, scripted effects, scripted triggers, localisation, or HOI4 error logs. Prefer CWTools for editor validation when available, and use the bundled HOI4 tooling for mod-root discovery, ID inventory, localisation audits, and log summaries."
---

# HOI4 Modding

Help with Hearts of Iron IV modding in a way that stays close to real project structure, existing naming conventions, and the game's validation constraints.

## Quick start

- First locate the mod root. Prefer a directory that contains `descriptor.mod` and one or more of `common/`, `events/`, or `localisation/`. If the user does not provide a path, use the bundled HOI4 MCP or scripts to search for it.
- Before editing, inspect nearby files and copy the project's existing `namespace`, tag prefix, and file naming patterns. Extend adjacent content instead of inventing parallel structures.
- After edits, always run the content inventory and localisation audit. If the user has a current `error.log`, summarize it before guessing at fixes.
- Treat CWTools as the primary syntax and scope validator in the editor when it is available. The bundled tools are best for structure checks, missing localisation, and log-driven triage.

## Workflow

1. Identify the gameplay primitive that best matches the request.
2. Read one or two neighboring files that already implement the same kind of content.
3. Implement the full content bundle instead of a partial snippet.
4. Validate IDs, localisation coverage, and error-log output.
5. Report what changed, where to test it, and any remaining assets or balancing work.

## Content bundle map

- Focus tree work:
  Update `common/national_focus/` and the matching localisation file. If the focus unlocks events, ideas, or decisions, create those companion files in the same pass. If the project uses custom icons, also check `gfx/interface/goals/`.
- Event chains:
  Update `events/` plus localisation. Keep namespaces stable and unique. Add hooks such as `on_actions` only when the design really needs automatic firing.
- Decisions:
  Update `common/decisions/` plus localisation. If the decision depends on reusable logic, move that logic into `common/scripted_triggers/` or `common/scripted_effects/`.
- Ideas and spirits:
  Update `common/ideas/` plus localisation, and check whether the project expects icon assets or scripted modifiers.
- Reusable systems:
  Prefer `common/scripted_effects/` and `common/scripted_triggers/` over copy-pasting the same logic across events, focuses, and decisions.
- AI behavior:
  Keep AI changes explicit. Use `ai_will_do`, AI-only triggers, or `common/ai_strategy_plans/` when the design depends on country behavior instead of player interaction.

## Quality rules

- Keep IDs and namespaces collision-free. Reuse the project's prefix patterns.
- Every focus should have a base localisation key and a `_desc` key.
- Every event should have a namespace and at least `.t` and `.d` localisation keys. Option names and custom tooltips also need localisation.
- Localisation files should stay in the appropriate language folder and keep a valid language header such as `l_english:`.
- Do not invent country tags, state IDs, or scripted variables if the mod already has conventions or reference files that define them. Search first.
- Prefer small, composable scripted helpers over giant one-off blocks when logic is reused.

## Tooling

Use the local HOI4 MCP server when available:

- `find_mod_roots` to discover likely mod roots from a search directory.
- `inspect_mod_structure` to summarize a mod's structure and content counts.
- `inventory_content_ids` to spot duplicate focus IDs, event IDs, namespaces, and other symbol collisions.
- `find_missing_localisation` to find missing or duplicated localisation keys.
- `summarize_hoi4_error_log` to group error log lines before debugging.

If the MCP server is not available, run the packaged CLI directly from this repository:

- `python -m pip install -e .`
- `hoi4-find-mod-roots <search_root>`
- `hoi4-inspect-mod <mod_root>`
- `hoi4-inventory-ids <mod_root>`
- `hoi4-audit-localisation <mod_root>`
- `hoi4-summarize-log <error.log>`

## Reference map

Read only what you need:

- `references/folder-map.md` for where each HOI4 content type usually lives.
- `references/content-bundles.md` for what files should move together for focuses, events, decisions, and ideas.
- `references/debugging.md` for the validation loop and common failure modes.

## Repository integration

This skill is meant to live inside a Codex skills directory after cloning the repository. For Codex users, copy or symlink `skills/hoi4-modding/` into your local skills folder and register the MCP command shown in `README.md`.
