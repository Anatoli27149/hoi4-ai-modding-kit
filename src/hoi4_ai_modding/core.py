from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


LOC_FIELDS = {
    "available_tooltip",
    "bypass_tooltip",
    "complete_tooltip",
    "custom_effect_tooltip",
    "custom_trigger_tooltip",
    "desc",
    "hidden_effect_tooltip",
    "mission_text",
    "name",
    "news_desc_long",
    "select_effect_tooltip",
    "text",
    "title",
    "tooltip",
    "unavailable",
    "visible_tooltip",
}
# 这些值看起来像标识符，但通常不是 localisation key，本地化审计时要跳过。
NON_LOC_VALUES = {
    "always",
    "and",
    "else",
    "english",
    "false",
    "from",
    "limit",
    "no",
    "not",
    "or",
    "prev",
    "random",
    "root",
    "this",
    "true",
    "yes",
}
# 这些块名多半是容器或控制流，不应该被当成可本地化内容 ID。
HEURISTIC_SKIP_KEYS = {
    "abort",
    "ai_will_do",
    "allow",
    "allowed",
    "available",
    "available_if_capitulated",
    "bypass",
    "cancel_effect",
    "complete_effect",
    "completion_reward",
    "country",
    "country_decisions",
    "decisions",
    "decision_categories",
    "decision_category",
    "effect",
    "else",
    "else_if",
    "generic_decisions",
    "hidden_effect",
    "ideas",
    "if",
    "immediate",
    "limit",
    "modifier",
    "not",
    "on_map_mode",
    "option",
    "or",
    "potential",
    "random",
    "random_list",
    "remove_effect",
    "state_decisions",
    "target_array",
    "targets",
    "trigger",
    "visible",
}
LANGUAGE_HEADER_RE = re.compile(r"^\ufeff?\s*l_([a-z_]+)\s*:\s*$", re.IGNORECASE)
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.:-]+)\s*:\d+", re.MULTILINE)
ASSIGNMENT_RE = re.compile(
    r"\b(?P<field>"
    + "|".join(sorted(LOC_FIELDS))
    + r")\s*=\s*(?P<quote>\"?)(?P<value>[A-Za-z0-9_.:-]+)(?P=quote)",
    re.IGNORECASE,
)
BLOCK_KEY_RE = re.compile(r"(?m)^\s*([A-Za-z0-9_.-]+)\s*=\s*\{")
EVENT_ID_RE = re.compile(r"\bid\s*=\s*([A-Za-z0-9_.-]+)")
NAMESPACE_RE = re.compile(r"\badd_namespace\s*=\s*([A-Za-z0-9_.-]+)")


def resolve_path(path: str) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate


def normalize_mod_root(path: str) -> Path:
    candidate = resolve_path(path)
    if candidate.is_file():
        candidate = candidate.parent
    return candidate


def _read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def _iter_files(root: Path, relative_dir: str, suffixes: Iterable[str] = (".txt",)) -> list[Path]:
    base = root / relative_dir
    if not base.exists():
        return []
    suffix_set = {suffix.lower() for suffix in suffixes}
    results: list[Path] = []
    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in suffix_set:
            results.append(path)
    return sorted(results)


def _extract_block_bodies(text: str, block_name: str) -> list[str]:
    bodies: list[str] = []
    pattern = re.compile(rf"\b{re.escape(block_name)}\s*=\s*\{{")
    start = 0
    while True:
        match = pattern.search(text, start)
        if not match:
            break
        brace_index = text.find("{", match.start())
        if brace_index == -1:
            break
        depth = 0
        # 用最轻量的花括号配平来抽块，足够覆盖 HOI4 脚本常见结构。
        for index in range(brace_index, len(text)):
            char = text[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    bodies.append(text[brace_index + 1 : index])
                    start = index + 1
                    break
        else:
            break
    return bodies


def _collect_focus_ids(paths: Iterable[Path], root: Path) -> dict[str, list[str]]:
    values: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        text = _read_text(path)
        rel = _relative(path, root)
        # focus_tree 本身也可能带 id，但真正需要防冲突的是 focus/shared_focus 的 id。
        for block_name in ("focus", "shared_focus"):
            for body in _extract_block_bodies(text, block_name):
                match = EVENT_ID_RE.search(body)
                if match:
                    values[match.group(1).strip()].append(rel)
    return dict(values)


def find_mod_roots(search_root: str, max_depth: int = 4, max_results: int = 25) -> dict:
    root = resolve_path(search_root)
    if not root.exists():
        raise FileNotFoundError(f"Path not found: {root}")

    matches: list[dict] = []
    seen: set[Path] = set()

    # 如果传入路径本身就是 mod 根目录，优先直接返回它，避免只搜子目录。
    if (root / "descriptor.mod").exists():
        seen.add(root)
        matches.append(
            {
                "mod_root": str(root),
                "depth": 0,
                "has_common": (root / "common").exists(),
                "has_events": (root / "events").exists(),
                "has_localisation": (root / "localisation").exists(),
            }
        )
        if len(matches) >= max_results:
            return {"search_root": str(root), "matches": matches}

    for descriptor in root.rglob("descriptor.mod"):
        depth = len(descriptor.relative_to(root).parts) - 1
        if depth > max_depth:
            continue
        mod_root = descriptor.parent
        if mod_root in seen:
            continue
        seen.add(mod_root)
        matches.append(
            {
                "mod_root": str(mod_root),
                "depth": depth,
                "has_common": (mod_root / "common").exists(),
                "has_events": (mod_root / "events").exists(),
                "has_localisation": (mod_root / "localisation").exists(),
            }
        )
        if len(matches) >= max_results:
            return {"search_root": str(root), "matches": matches}

    probable: list[dict] = []
    for directory in sorted(path for path in root.rglob("*") if path.is_dir()):
        depth = len(directory.relative_to(root).parts)
        if depth > max_depth:
            continue
        signals = sum(
            [
                (directory / "common").exists(),
                (directory / "events").exists(),
                (directory / "localisation").exists(),
            ]
        )
        if signals >= 2:
            probable.append(
                {
                    "mod_root": str(directory),
                    "depth": depth,
                    "has_common": (directory / "common").exists(),
                    "has_events": (directory / "events").exists(),
                    "has_localisation": (directory / "localisation").exists(),
                }
            )
            if len(probable) >= max_results:
                break

    return {"search_root": str(root), "matches": matches or probable}


def inspect_mod_structure(mod_root: str) -> dict:
    root = normalize_mod_root(mod_root)
    if not root.exists():
        raise FileNotFoundError(f"Mod root not found: {root}")

    folders = {
        "descriptor": root / "descriptor.mod",
        "common": root / "common",
        "focuses": root / "common" / "national_focus",
        "events": root / "events",
        "decisions": root / "common" / "decisions",
        "ideas": root / "common" / "ideas",
        "scripted_effects": root / "common" / "scripted_effects",
        "scripted_triggers": root / "common" / "scripted_triggers",
        "on_actions": root / "common" / "on_actions",
        "ai_strategy_plans": root / "common" / "ai_strategy_plans",
        "localisation": root / "localisation",
        "english_localisation": root / "localisation" / "english",
        "focus_icons": root / "gfx" / "interface" / "goals",
        "event_pictures": root / "gfx" / "event_pictures",
    }

    content_counts = {
        "focus_files": len(_iter_files(root, "common/national_focus")),
        "event_files": len(_iter_files(root, "events")),
        "decision_files": len(_iter_files(root, "common/decisions")),
        "idea_files": len(_iter_files(root, "common/ideas")),
        "scripted_effect_files": len(_iter_files(root, "common/scripted_effects")),
        "scripted_trigger_files": len(_iter_files(root, "common/scripted_triggers")),
        "on_action_files": len(_iter_files(root, "common/on_actions")),
        "ai_strategy_files": len(_iter_files(root, "common/ai_strategy_plans")),
        "localisation_files": len(_iter_files(root, "localisation", suffixes=(".yml", ".yaml"))),
        "gfx_files": len(_iter_files(root, "gfx", suffixes=(".dds", ".tga", ".png", ".gfx"))),
    }

    languages: Counter[str] = Counter()
    for path in _iter_files(root, "localisation", suffixes=(".yml", ".yaml")):
        lines = _read_text(path).splitlines()
        if not lines:
            continue
        match = LANGUAGE_HEADER_RE.search(lines[0])
        if match:
            languages[match.group(1).lower()] += 1

    present = [label for label, path in folders.items() if path.exists()]
    missing = [label for label, path in folders.items() if not path.exists()]

    return {
        "mod_root": str(root),
        "present_paths": present,
        "missing_paths": missing,
        "content_counts": content_counts,
        "localisation_languages": dict(languages),
        "looks_like_mod_root": folders["descriptor"].exists() or content_counts["localisation_files"] > 0,
    }


def _collect_assignments(paths: Iterable[Path], regex: re.Pattern[str], root: Path) -> dict[str, list[str]]:
    values: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        for match in regex.finditer(_read_text(path)):
            values[match.group(1).strip()].append(_relative(path, root))
    return dict(values)


def _collect_block_keys(paths: Iterable[Path], root: Path) -> dict[str, list[str]]:
    values: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        for token in BLOCK_KEY_RE.findall(_read_text(path)):
            lowered = token.lower()
            if lowered in HEURISTIC_SKIP_KEYS:
                continue
            # 很短的全大写块名更像常量或保留标记，误报价值不高。
            if token.isupper() and len(token) <= 4:
                continue
            values[token].append(_relative(path, root))
    return dict(values)


def _duplicates(mapping: dict[str, list[str]], limit: int = 100) -> list[dict]:
    rows: list[dict] = []
    for key, paths in sorted(mapping.items()):
        unique_paths = sorted(set(paths))
        if len(unique_paths) > 1:
            rows.append({"key": key, "count": len(unique_paths), "paths": unique_paths})
            if len(rows) >= limit:
                break
    return rows


def inventory_content_ids(mod_root: str, sample_limit: int = 20, duplicate_limit: int = 100) -> dict:
    root = normalize_mod_root(mod_root)
    if not root.exists():
        raise FileNotFoundError(f"Mod root not found: {root}")

    sections = {
        "focus_ids": _collect_focus_ids(_iter_files(root, "common/national_focus"), root),
        "event_ids": _collect_assignments(_iter_files(root, "events"), EVENT_ID_RE, root),
        "event_namespaces": _collect_assignments(_iter_files(root, "events"), NAMESPACE_RE, root),
        "heuristic_decision_blocks": _collect_block_keys(_iter_files(root, "common/decisions"), root),
        "heuristic_idea_blocks": _collect_block_keys(_iter_files(root, "common/ideas"), root),
        "scripted_effects": _collect_block_keys(_iter_files(root, "common/scripted_effects"), root),
        "scripted_triggers": _collect_block_keys(_iter_files(root, "common/scripted_triggers"), root),
    }

    return {
        "mod_root": str(root),
        "counts": {name: len(values) for name, values in sections.items()},
        "duplicates": {name: _duplicates(values, limit=duplicate_limit) for name, values in sections.items()},
        "samples": {
            name: [
                {"key": key, "paths": sorted(set(paths))}
                for key, paths in list(sorted(values.items()))[:sample_limit]
            ]
            for name, values in sections.items()
        },
        "notes": [
            "Decision and idea inventories are heuristic and may include some false positives from nested blocks.",
        ],
    }


def _collect_localisation(mod_root: Path, language: str) -> tuple[dict[str, list[str]], list[dict]]:
    language = language.lower()
    found: dict[str, list[str]] = defaultdict(list)
    duplicates: list[dict] = []

    for path in _iter_files(mod_root, "localisation", suffixes=(".yml", ".yaml")):
        lines = _read_text(path).splitlines()
        if not lines:
            continue
        match = LANGUAGE_HEADER_RE.search(lines[0])
        if match and match.group(1).lower() != language:
            continue
        for key in LOC_KEY_RE.findall("\n".join(lines)):
            found[key].append(_relative(path, mod_root))

    for key, paths in sorted(found.items()):
        unique_paths = sorted(set(paths))
        if len(unique_paths) > 1:
            duplicates.append({"key": key, "count": len(unique_paths), "paths": unique_paths})

    return dict(found), duplicates


def _looks_like_loc_value(value: str) -> bool:
    lowered = value.lower()
    if lowered in NON_LOC_VALUES:
        return False
    if "/" in value or "\\" in value:
        return False
    if re.fullmatch(r"-?\d+(\.\d+)?", value):
        return False
    if lowered.startswith(("gfx_", "sprite_", "sound_", "flag_", "modifier_")):
        return False
    return "." in value or "_" in value


def _collect_expected_localisation(root: Path) -> dict[str, list[dict]]:
    expected: dict[str, list[dict]] = defaultdict(list)

    for focus_id, paths in _collect_focus_ids(_iter_files(root, "common/national_focus"), root).items():
        for rel in sorted(set(paths)):
            expected[focus_id].append({"reason": "focus_name", "source": rel})
            expected[f"{focus_id}_desc"].append({"reason": "focus_desc", "source": rel})

    for path in _iter_files(root, "events"):
        rel = _relative(path, root)
        text = _read_text(path)
        # 事件最稳定的预期 key 是 .t 和 .d，其他 key 走启发式补充。
        for event_id in EVENT_ID_RE.findall(text):
            expected[f"{event_id}.t"].append({"reason": "event_title", "source": rel})
            expected[f"{event_id}.d"].append({"reason": "event_desc", "source": rel})
        for match in ASSIGNMENT_RE.finditer(text):
            value = match.group("value")
            if _looks_like_loc_value(value):
                expected[value].append({"reason": match.group("field").lower(), "source": rel})

    for relative_dir, reason in (
        ("common/decisions", "decision_or_category"),
        ("common/ideas", "idea_or_trait"),
    ):
        for path in _iter_files(root, relative_dir):
            rel = _relative(path, root)
            text = _read_text(path)
            # 决议和 idea 的块名很常直接就是 localisation key，这里做启发式收集。
            for token in BLOCK_KEY_RE.findall(text):
                if token.lower() in HEURISTIC_SKIP_KEYS:
                    continue
                if "." not in token and "_" not in token:
                    continue
                expected[token].append({"reason": reason, "source": rel})
            for match in ASSIGNMENT_RE.finditer(text):
                value = match.group("value")
                if _looks_like_loc_value(value):
                    expected[value].append({"reason": match.group("field").lower(), "source": rel})

    for relative_dir in ("common/scripted_effects", "common/scripted_triggers"):
        for path in _iter_files(root, relative_dir):
            rel = _relative(path, root)
            for match in ASSIGNMENT_RE.finditer(_read_text(path)):
                value = match.group("value")
                if _looks_like_loc_value(value):
                    expected[value].append({"reason": match.group("field").lower(), "source": rel})

    return dict(expected)


def find_missing_localisation(mod_root: str, language: str = "english", limit: int = 200) -> dict:
    root = normalize_mod_root(mod_root)
    if not root.exists():
        raise FileNotFoundError(f"Mod root not found: {root}")

    present, duplicate_keys = _collect_localisation(root, language)
    expected = _collect_expected_localisation(root)

    missing: list[dict] = []
    for key, sources in sorted(expected.items()):
        if key in present:
            continue
        missing.append({"key": key, "references": sources[:5]})
        if len(missing) >= limit:
            break

    return {
        "mod_root": str(root),
        "language": language.lower(),
        "present_key_count": len(present),
        "expected_key_count": len(expected),
        "missing_count": len([key for key in expected if key not in present]),
        "missing": missing,
        "duplicate_keys": duplicate_keys[:limit],
        "notes": [
            "Expected localisation uses a mix of explicit references and HOI4-specific heuristics for focuses, events, decisions, and ideas.",
        ],
    }


ERROR_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("missing_localisation", re.compile(r"loca(?:l|liz)", re.IGNORECASE)),
    ("unknown_effect", re.compile(r"unknown effect", re.IGNORECASE)),
    ("unknown_trigger", re.compile(r"unknown trigger", re.IGNORECASE)),
    ("invalid_scope", re.compile(r"invalid scope|scope", re.IGNORECASE)),
    ("missing_file_or_asset", re.compile(r"could not find|error opening|failed to open", re.IGNORECASE)),
    ("parser_or_syntax", re.compile(r"unexpected token|parser error|malformed", re.IGNORECASE)),
)


def summarize_error_log(log_path: str, limit: int = 20) -> dict:
    path = resolve_path(log_path)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    lines = [line.strip() for line in _read_text(path).splitlines() if line.strip()]
    category_counts: Counter[str] = Counter()
    category_samples: dict[str, list[str]] = defaultdict(list)

    inspected = lines[-5000:]
    for line in inspected:
        category = "other"
        # 先按高价值问题分组，便于决定“先修缺 loc”还是“先修 effect/trigger”。
        for name, pattern in ERROR_PATTERNS:
            if pattern.search(line):
                category = name
                break
        category_counts[category] += 1
        if len(category_samples[category]) < 10 and line not in category_samples[category]:
            category_samples[category].append(line)

    categories = [
        {
            "category": name,
            "count": count,
            "samples": category_samples[name],
        }
        for name, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]

    return {
        "log_path": str(path),
        "total_non_empty_lines": len(lines),
        "inspected_lines": len(inspected),
        "categories": categories,
    }


def to_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
