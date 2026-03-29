# Project Spec

This repository packages the "best practical setup" for AI-assisted Hearts of Iron IV modding.

## Core design

The stack is deliberately split into three roles.

## 1. Editor validation

`VS Code + CWTools`

This catches the problems AI is worst at noticing by itself:

- Syntax errors
- Scope errors
- Broken references
- Some localisation and asset issues

## 2. AI workflow control

`skills/hoi4-modding`

The skill is responsible for how the AI works:

- Inspect neighboring files before inventing structure
- Preserve naming and namespace conventions
- Generate complete content bundles
- Validate after editing
- Report testing and remaining work clearly

## 3. Local machine tooling

`src/hoi4_ai_modding`

The Python package provides both CLI commands and an MCP server for:

- Mod-root discovery
- Structure inspection
- ID and namespace inventory
- Localisation auditing
- Error-log summarization

## Content bundles

The workflow assumes that content should be changed in bundles, not as isolated files.

- Focus work should usually include localisation and any companion events, ideas, or decisions.
- Event work should include namespace discipline, localisation, and trigger wiring.
- Decision work should include localisation and reusable scripted helpers when logic repeats.
- Idea work should include localisation and any dependent scripted hooks.

## Quality rules

- Reuse project prefixes and namespace conventions.
- Keep IDs collision-free.
- Always audit localisation after changes.
- Prefer scripted helpers over copy-pasted logic.
- Use the game log and CWTools as the main sources of truth when behavior disagrees with assumptions.

## Non-goals

- This project does not try to be a full HOI4 schema database.
- This project does not replace the game's own documentation HTML pages.
- This project does not enforce one single mod architecture across all projects.

Instead, it provides strong defaults and a dependable workflow.
