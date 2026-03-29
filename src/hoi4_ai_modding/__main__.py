from __future__ import annotations

import argparse
import sys

from .cli import (
    audit_localisation_main,
    find_mod_roots_main,
    inspect_mod_structure_main,
    inventory_ids_main,
    serve_mcp_main,
    summarize_error_log_main,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="HOI4 AI Modding Kit command runner.")
    parser.add_argument(
        "command",
        choices=[
            "find-mod-roots",
            "inspect-mod",
            "inventory-ids",
            "audit-localisation",
            "summarize-log",
            "serve-mcp",
        ],
        help="Command to run.",
    )
    args, remainder = parser.parse_known_args()

    sys.argv = [sys.argv[0], *remainder]

    dispatch = {
        "find-mod-roots": find_mod_roots_main,
        "inspect-mod": inspect_mod_structure_main,
        "inventory-ids": inventory_ids_main,
        "audit-localisation": audit_localisation_main,
        "summarize-log": summarize_error_log_main,
        "serve-mcp": serve_mcp_main,
    }
    dispatch[args.command]()


if __name__ == "__main__":
    main()
