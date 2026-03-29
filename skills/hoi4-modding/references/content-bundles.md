# Content Bundles

Use these checklists to avoid half-finished HOI4 changes.

## Focus bundle

- Edit or create the focus tree file in `common/national_focus/`.
- Add the focus name localisation key.
- Add the focus description localisation key with the `_desc` suffix.
- If the focus fires events, grants ideas, or unlocks decisions, add those companion files in the same pass.
- If the mod uses custom icons, confirm the icon path and asset exist.

## Event bundle

- Keep the event in `events/`.
- Use a stable namespace and avoid collisions with other event files.
- Add `.t` and `.d` localisation keys for every event ID.
- Add option localisation keys such as `.a`, `.b`, and custom tooltip keys when present.
- If the event is triggered automatically, wire it through the correct hook such as a decision, focus reward, or `on_actions`.

## Decision bundle

- Add or edit the category in `common/decisions/`.
- Add localisation for the category and each decision.
- Move reused conditions or effects into scripted helpers instead of copying them.
- Check AI weighting and cooldown logic if the decision should be AI-visible.

## Idea bundle

- Add or edit the idea in `common/ideas/`.
- Add localisation for the idea key.
- If the idea has scripted interactions, keep the scripted pieces close and clearly named.
- If the mod uses custom art, verify the icon reference.

## Country bundle

- Register the tag in `common/country_tags/`.
- Create or update the country base file in `common/countries/`.
- Create or update the country history file in `history/countries/`.
- Add localisation for base names, ideology variants, and adjectives.
- Confirm flag assets exist in `gfx/flags/` and the `small/` and `medium/` subfolders when the project expects them.
- If the country uses explicit characters, update `common/characters/` in the same pass.
- If the country needs units at start, confirm OOB references instead of leaving dangling `set_oob` calls.

## State bundle

- Create or update the state file in `history/states/`.
- Add the matching `STATE_<id>` localisation key.
- Validate province ownership so each province belongs to exactly one state.
- Keep province buildings under a province block and state buildings at the state level.
- Check shared-slot pressure before assigning factories, refineries, silos, rocket sites, or reactors.

## Map and region bundle

- If the request only redistributes existing provinces, prefer a validation or overlay pass before editing map assets.
- If the request adds provinces or changes province borders, update `map/provinces.bmp`, `map/definition.csv`, and the affected `history/states/` files together.
- Update `map/adjacencies.csv`, `strategic regions`, and `map/buildings.txt` only when the design actually changes those systems.
- Do not treat `map/buildings.txt` as the primary source of starting building counts; state history is still the main source of truth.

## Reusable systems

- Use scripted effects for reusable effect logic.
- Use scripted triggers for reusable conditions.
- Prefer references between systems over duplicating long logic blocks.

## Choosing the primitive

- Country progression or policy branching usually belongs in focuses.
- Repeatable actions, timed missions, or player choice hubs usually belong in decisions.
- One-shot narrative moments and branching scenes usually belong in events.
- Persistent modifiers and advisors usually belong in ideas.
