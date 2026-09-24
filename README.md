# Ctrl Notes for AI agents

Let your coding agent search, read and edit your Obsidian vault through
[Ctrl Notes](https://ctrlnotes.app).

This repository is the plugin. It holds no code that runs on your machine. It
contains:

- **A connection** to the Ctrl Notes MCP server at `https://mcp.ctrlnotes.app/mcp`.
  You sign in through your browser the first time your agent uses it.
- **A skill**, [`skills/ctrlnotes`](skills/ctrlnotes/SKILL.md), that tells the
  agent how to use the three tools safely: look before editing, edit the smallest
  thing, and ask before deleting anything.

## What it can do

The server exposes one vault through three tools.

| Tool | What it does | Changes your vault? |
| --- | --- | --- |
| `query` | Runs a read-only SQL query over your notes, tags, links and Bases | No |
| `open` | Returns one note with line anchors and a version stamp | No |
| `apply` | Edits, creates, renames or deletes notes in one transaction | Yes |

When you sign in, you choose which vault the agent reaches and whether it may
edit. Access is read-only unless you grant write access, and a read-only
connection has `apply` refused outright. Edits are guarded too: if a note
changed on another device while the agent was working, `apply` refuses rather
than overwriting it.

## Before you install

You need a Ctrl Notes account with a vault, synced from Obsidian. Sign up at
[ctrlnotes.app](https://ctrlnotes.app).

## Install

### Claude Code

```text
/plugin marketplace add ctrlnotes/agent-plugins
/plugin install ctrlnotes@ctrlnotes
```

### Codex

```bash
codex plugin marketplace add ctrlnotes/agent-plugins
codex plugin add ctrlnotes@ctrlnotes
```

### Gemini CLI

```bash
gemini extensions install https://github.com/ctrlnotes/agent-plugins
```

### Other agents

Agents that read the [Agent Plugins 1.0](https://agent-plugins.org) format, or
Claude Code's plugin format, can install from this repository's URL.

Any other MCP client can connect to the server directly. It speaks Streamable
HTTP and signs you in with OAuth:

```text
https://mcp.ctrlnotes.app/mcp
```

For example, in opencode's `opencode.json`:

```json
{
  "mcp": {
    "ctrlnotes": { "type": "remote", "url": "https://mcp.ctrlnotes.app/mcp" }
  }
}
```

## Try it

- "What did I write about the Q3 launch last month?"
- "Which notes tagged #reading don't link to anything yet?"
- "Add 'Call the landlord' as a task under Today in my daily note."
- "Move projects/alpha.md into projects/archive and keep every link to it working."

## Troubleshooting

- **The agent asks you to sign in again.** Your session with Ctrl Notes expired
  or was revoked. Reconnect the `ctrlnotes` server from your agent's MCP
  settings (`/mcp` in Claude Code).
- **Edits are refused as read-only.** Access is read-only unless you grant
  write access when you sign in. Reconnect and choose write access if you want
  the agent to edit.
- **The tools are missing.** Check that the plugin is enabled, then restart the
  agent. A client reads the tool list when it connects.

## Privacy

The plugin sends nothing by itself. Your agent sends your queries and edits to
Ctrl Notes, which answers from your own vault. See the
[privacy policy](https://ctrlnotes.app/privacy) and
[terms](https://ctrlnotes.app/tos).

## Support

Open an [issue](https://github.com/ctrlnotes/agent-plugins/issues). To report
a security problem, see [SECURITY.md](SECURITY.md).

## Releasing

Every agent above offers an update only when the version changes, so a change to
anything that ships needs a new version in `plugin.json`,
`.claude-plugin/plugin.json` and `gemini-extension.json`. CI fails a pull request
that forgets, and fails if the three disagree.

## Licence

[MIT](LICENSE)
