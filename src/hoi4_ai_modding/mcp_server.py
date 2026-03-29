from __future__ import annotations

from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .core import (
    find_missing_localisation,
    find_mod_roots,
    inspect_mod_structure,
    inventory_content_ids,
    summarize_error_log,
)


mcp = FastMCP(
    name="hoi4-modding",
    instructions=(
        # MCP 层尽量保持薄，只做参数接入和结构化输出。
        "Inspect Hearts of Iron IV mod folders, inventory IDs, audit localisation, "
        "and summarize HOI4 error logs."
    ),
)


@mcp.tool(
    name="find_mod_roots",
    description="Search a directory for likely Hearts of Iron IV mod roots by looking for descriptor.mod and standard mod folders.",
    structured_output=True,
)
def tool_find_mod_roots(
    search_root: Annotated[
        str,
        Field(description="Directory to search for Hearts of Iron IV mod roots."),
    ],
    max_depth: Annotated[
        int,
        Field(description="Maximum depth to search below the search root.", ge=1, le=8),
    ] = 4,
    max_results: Annotated[
        int,
        Field(description="Maximum number of matches to return.", ge=1, le=100),
    ] = 25,
) -> dict[str, Any]:
    return find_mod_roots(search_root, max_depth=max_depth, max_results=max_results)


@mcp.tool(
    name="inspect_mod_structure",
    description="Summarize the structure of a Hearts of Iron IV mod root and count major content folders.",
    structured_output=True,
)
def tool_inspect_mod_structure(
    mod_root: Annotated[
        str,
        Field(description="Path to the Hearts of Iron IV mod root."),
    ],
) -> dict[str, Any]:
    return inspect_mod_structure(mod_root)


@mcp.tool(
    name="inventory_content_ids",
    description="Inventory focus IDs, event IDs, namespaces, and other HOI4 symbols to spot duplicates before debugging.",
    structured_output=True,
)
def tool_inventory_content_ids(
    mod_root: Annotated[
        str,
        Field(description="Path to the Hearts of Iron IV mod root."),
    ],
    sample_limit: Annotated[
        int,
        Field(description="Number of sample entries to include per section.", ge=1, le=100),
    ] = 20,
    duplicate_limit: Annotated[
        int,
        Field(description="Maximum duplicate entries to include per section.", ge=1, le=200),
    ] = 100,
) -> dict[str, Any]:
    return inventory_content_ids(mod_root, sample_limit=sample_limit, duplicate_limit=duplicate_limit)


@mcp.tool(
    name="find_missing_localisation",
    description="Compare HOI4 content against localisation files to find missing or duplicated localisation keys.",
    structured_output=True,
)
def tool_find_missing_localisation(
    mod_root: Annotated[
        str,
        Field(description="Path to the Hearts of Iron IV mod root."),
    ],
    language: Annotated[
        str,
        Field(description="Language name from the localisation header, such as english."),
    ] = "english",
    limit: Annotated[
        int,
        Field(description="Maximum number of missing or duplicate keys to include.", ge=1, le=500),
    ] = 200,
) -> dict[str, Any]:
    return find_missing_localisation(mod_root, language=language, limit=limit)


@mcp.tool(
    name="summarize_hoi4_error_log",
    description="Group repeated Hearts of Iron IV error.log lines into categories for faster debugging.",
    structured_output=True,
)
def tool_summarize_error_log(
    log_path: Annotated[
        str,
        Field(description="Path to a Hearts of Iron IV error.log file."),
    ],
    limit: Annotated[
        int,
        Field(description="Maximum number of categories to include.", ge=1, le=100),
    ] = 20,
) -> dict[str, Any]:
    return summarize_error_log(log_path, limit=limit)


if __name__ == "__main__":
    mcp.run()
