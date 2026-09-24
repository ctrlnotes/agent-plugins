"""Hold the per-agent manifests to one another.

Each agent reads its own manifest, so nothing but this script notices when
they drift: a version bumped in one file and not the others, or an MCP URL
changed for Claude Code and left stale for Gemini.

Usage: check.py <agent-plugins schema dir>
"""

import json
import re
import sys
from pathlib import Path

import jsonschema

NAME = "ctrlnotes"
MCP_URL = "https://mcp.ctrlnotes.app/mcp"

errors = []


def load(path):
    return json.loads(Path(path).read_text())


def expect(what, actual, wanted):
    if actual != wanted:
        errors.append(f"{what}: {actual!r}, expected {wanted!r}")


schemas = Path(sys.argv[1])
agent_plugin = load("plugin.json")
agent_mcp = load("mcp.json")
for doc, schema in [(agent_plugin, "plugin"), (agent_mcp, "mcp")]:
    try:
        jsonschema.validate(doc, load(schemas / f"{schema}.schema.json"))
    except jsonschema.ValidationError as e:
        errors.append(f"{schema}.json does not match Agent Plugins 1.0: {e.message}")

claude_plugin = load(".claude-plugin/plugin.json")
claude_mcp = load(".mcp.json")
claude_market = load(".claude-plugin/marketplace.json")
codex_market = load(".agents/plugins/marketplace.json")
gemini = load("gemini-extension.json")

for what, name in [
    ("plugin.json name", agent_plugin["name"]),
    (".claude-plugin/plugin.json name", claude_plugin["name"]),
    ("gemini-extension.json name", gemini["name"]),
    (".claude-plugin/marketplace.json name", claude_market["name"]),
    (".claude-plugin/marketplace.json plugin", claude_market["plugins"][0]["name"]),
    (".agents/plugins/marketplace.json name", codex_market["name"]),
    (".agents/plugins/marketplace.json plugin", codex_market["plugins"][0]["name"]),
]:
    expect(what, name, NAME)

version = agent_plugin.get("version")
if not version:
    errors.append("plugin.json has no version")
expect(".claude-plugin/plugin.json version", claude_plugin.get("version"), version)
expect("gemini-extension.json version", gemini.get("version"), version)

expect("mcp.json url", agent_mcp["mcpServers"][NAME]["url"], MCP_URL)
expect(".mcp.json url", claude_mcp["mcpServers"][NAME]["url"], MCP_URL)
expect("gemini-extension.json httpUrl", gemini["mcpServers"][NAME]["httpUrl"], MCP_URL)

description = agent_plugin.get("description")
for what, d in [
    (".claude-plugin/plugin.json description", claude_plugin.get("description")),
    ("gemini-extension.json description", gemini.get("description")),
    (".claude-plugin/marketplace.json plugin description", claude_market["plugins"][0].get("description")),
]:
    expect(what, d, description)

# Agent Skills: `name` must match its directory, `description` at most 1024.
for skill in sorted(Path("skills").glob("*/SKILL.md")):
    front = re.match(r"---\n(.*?)\n---\n", skill.read_text(), re.S)
    if not front:
        errors.append(f"{skill}: no frontmatter")
        continue
    fields = dict(
        line.split(": ", 1) for line in front.group(1).splitlines() if ": " in line
    )
    expect(f"{skill} name", fields.get("name"), skill.parent.name)
    if not 1 <= len(fields.get("description", "")) <= 1024:
        errors.append(f"{skill}: description must be 1-1024 characters")

for e in errors:
    print(f"::error::{e}")
print(f"{len(errors)} problem(s); version {version}")
sys.exit(1 if errors else 0)
