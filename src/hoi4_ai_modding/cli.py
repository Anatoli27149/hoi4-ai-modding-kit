from __future__ import annotations

import argparse

from .core import (
    find_missing_localisation,
    find_mod_roots,
    inspect_mod_structure,
    inventory_content_ids,
    summarize_error_log,
    to_json,
)
from .mcp_server import mcp


def find_mod_roots_main() -> None:
    # 每个子命令都保持单一职责，方便后面既能做 CLI，也能包给别的工具调用。
    parser = argparse.ArgumentParser(description="Find likely Hearts of Iron IV mod roots.")
    parser.add_argument("search_root", help="Directory to search.")
    parser.add_argument("--max-depth", type=int, default=4, help="Maximum search depth from the search root.")
    parser.add_argument("--max-results", type=int, default=25, help="Maximum number of matches to return.")
    args = parser.parse_args()
    print(to_json(find_mod_roots(args.search_root, max_depth=args.max_depth, max_results=args.max_results)))


def inspect_mod_structure_main() -> None:
    parser = argparse.ArgumentParser(description="Summarize the structure of a Hearts of Iron IV mod.")
    parser.add_argument("mod_root", help="Path to the mod root.")
    args = parser.parse_args()
    print(to_json(inspect_mod_structure(args.mod_root)))


def inventory_ids_main() -> None:
    parser = argparse.ArgumentParser(description="Inventory Hearts of Iron IV content IDs and namespaces.")
    parser.add_argument("mod_root", help="Path to the mod root.")
    parser.add_argument("--sample-limit", type=int, default=20, help="Number of sample entries per section.")
    parser.add_argument("--duplicate-limit", type=int, default=100, help="Maximum duplicates to report per section.")
    args = parser.parse_args()
    print(
        to_json(
            inventory_content_ids(
                args.mod_root,
                sample_limit=args.sample_limit,
                duplicate_limit=args.duplicate_limit,
            )
        )
    )


def audit_localisation_main() -> None:
    parser = argparse.ArgumentParser(description="Audit Hearts of Iron IV localisation coverage.")
    parser.add_argument("mod_root", help="Path to the mod root.")
    parser.add_argument("--language", default="english", help="Language name from the localisation header, such as english.")
    parser.add_argument("--limit", type=int, default=200, help="Maximum number of missing or duplicate keys to print.")
    args = parser.parse_args()
    print(to_json(find_missing_localisation(args.mod_root, language=args.language, limit=args.limit)))


def summarize_error_log_main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Hearts of Iron IV error.log categories.")
    parser.add_argument("log_path", help="Path to error.log.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of categories to print.")
    args = parser.parse_args()
    print(to_json(summarize_error_log(args.log_path, limit=args.limit)))


def serve_mcp_main() -> None:
    # MCP 模式下直接复用同一套核心逻辑，避免 CLI 和 MCP 分叉。
    mcp.run()
