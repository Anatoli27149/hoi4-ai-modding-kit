# Setup

This repository is meant to work in two modes:

- As a standalone CLI and local MCP toolset.
- As a Codex skill plus MCP integration for AI-assisted HOI4 work.

## Prerequisites

- Python 3.11 or newer
- VS Code if you want CWTools validation
- Hearts of Iron IV installed if you want to compare against local game files and documentation

## Python install

From the repository root:

```powershell
python -m pip install -e .
```

This exposes the following commands:

- `hoi4-find-mod-roots`
- `hoi4-inspect-mod`
- `hoi4-inventory-ids`
- `hoi4-audit-localisation`
- `hoi4-summarize-log`
- `hoi4-mcp-server`

If your Python user scripts directory is not on `PATH`, the module entry works too:

```powershell
python -m hoi4_ai_modding find-mod-roots "D:\Games\HOI4\mod"
python -m hoi4_ai_modding inspect-mod "D:\Games\HOI4\mod\my_mod"
python -m hoi4_ai_modding serve-mcp
```

## VS Code setup

Install the CWTools extension:

```powershell
code --install-extension tboby.cwtools-vscode
```

CWTools is the primary editor-time validator for HOI4 syntax, scopes, references, and some localisation issues.

## Codex setup

If you use Codex locally, run:

```powershell
.\tools\install_codex_integration.ps1
```

That script:

- Copies the `skills/hoi4-modding` bundle into your Codex skills folder
- Prints the MCP config block you should add if it is not already present

If you want to register the MCP manually, add this to your Codex config:

```toml
[mcp_servers.hoi4-modding]
command = "python"
args = ["-m", "hoi4_ai_modding.mcp_server"]
```

## Game documentation

For exact trigger and effect coverage in your installed game version, prefer the local HOI4 documentation files:

- `...\Hearts of Iron IV\documentation\triggers_documentation.html`
- `...\Hearts of Iron IV\documentation\effects_documentation.html`

Those files are the safest source for version-specific token support.
