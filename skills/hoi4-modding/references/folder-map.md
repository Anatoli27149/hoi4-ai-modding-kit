# Folder Map

Use this map when deciding where a new HOI4 feature belongs.

- `descriptor.mod`
  Mod metadata and the clearest signal that a directory is the mod root.
- `common/national_focus/`
  Focus trees and focus definitions.
- `common/country_tags/`
  Country tag registration and tag-to-file mapping.
- `common/countries/`
  Country colors, graphical cultures, and map presentation basics.
- `common/characters/`
  Character tokens, portraits, advisor roles, and leader definitions.
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
- `history/countries/`
  Country start setup such as capital, politics, popularity, ideas, OOB, research slots, convoys, and starting technologies.
- `history/states/`
  State ownership, cores, claims, provinces, manpower, resources, victory points, and starting buildings.
- `common/state_category/`
  Base shared building slots and state-category presets such as `rural`, `town`, and `metropolis`.
- `localisation/english/`
  English localisation files. Keep a valid `l_english:` header and UTF-8 with BOM when writing files for the game.
- `localisation/simp_chinese/`
  Simplified Chinese localisation when the project ships Chinese text.
- `gfx/interface/goals/`
  Custom focus icons and related interface assets.
- `gfx/event_pictures/`
  Event artwork when the project uses custom pictures.
- `gfx/flags/`
  Country flags and ideology-variant flags.
- `map/definition.csv`
  Province ID to RGB mapping.
- `map/provinces.bmp`
  Province boundaries. Touch only when province geometry actually changes.
- `map/buildings.txt`
  Map placement data for building visuals and special map objects.
- `map/adjacencies.csv`
  Special province-to-province adjacency links such as canals or straits.

When a request spans multiple systems, prefer implementing all companion files in one pass instead of leaving dangling references.
