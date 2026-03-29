# Debugging Loop

Use this order whenever HOI4 content does not behave as expected.

1. Confirm the mod root and file placement.
2. Inventory IDs and namespaces to catch duplicate symbols before deeper debugging.
3. Audit localisation so missing keys do not hide more important behavior problems.
4. Summarize `error.log` and group the errors before changing code.
5. Read one nearby working example and compare structure instead of guessing.
6. Fix the smallest root cause first, then re-run validation.

## Common failure modes

- Duplicate focus IDs or event IDs.
- Reused event namespaces across unrelated files.
- Missing localisation keys for focus descriptions, event titles, event descriptions, or decision names.
- Wrong scope for an effect or trigger.
- Missing hook wiring, such as a focus reward that never fires the event it references.
- Asset references that point to missing icons or pictures.
- Localisation files with an invalid language header or wrong encoding.

## Validation stance

- Prefer evidence from neighboring mod files, CWTools, and the game's error log over memory.
- If a bug could be either a logic problem or a missing asset or localisation problem, clear the data-quality issues first.
- When the error log is noisy, group repeated lines and fix the most frequent or most blocking category first.
