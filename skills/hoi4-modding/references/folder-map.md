# Folder Map

Use this map when deciding where a new HOI4 feature belongs.

- `descriptor.mod`
  Mod metadata and the clearest signal that a directory is the mod root.
- `common/national_focus/`
  Focus trees and focus definitions.
- `events/`
  Country events, news events, state events, and related namespaces.
- `common/decisions/`
  Decision categories and individual decisions.
- `common/ideas/`
  Ideas, national spirits, advisors, and other idea-like content.
- `common/scripted_effects/`
  Reusable effects that should not be duplicated across multiple content files.
- `common/scripted_triggers/`
  Reusable trigger logic for decisions, focuses, and events.
- `common/on_actions/`
  Automatic hooks that fire from game events. Use sparingly and document why.
- `common/ai_strategy_plans/`
  AI strategy definitions when balance or behavior depends on country AI priorities.
- `localisation/english/`
  English localisation files. Keep a valid `l_english:` header and UTF-8 with BOM when writing files for the game.
- `gfx/interface/goals/`
  Custom focus icons and related interface assets.
- `gfx/event_pictures/`
  Event artwork when the project uses custom pictures.

When a request spans multiple systems, prefer implementing all companion files in one pass instead of leaving dangling references.
