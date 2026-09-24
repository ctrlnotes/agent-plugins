---
name: ctrlnotes
description: Work with the user's Obsidian vault through the Ctrl Notes tools (query, open, apply). Use when the user asks about, searches, summarises or edits their notes, vault, daily notes, tags, links, backlinks or Obsidian Bases.
license: MIT
---

# Working with a Ctrl Notes vault

The `ctrlnotes` MCP server exposes one Obsidian vault through three tools. Each
tool's own description is the reference for its arguments; this is the order to
use them in.

## Find and read: `query`

`query` runs one SQL `SELECT` against an index of the vault. Its description is
generated from this vault's schema and carries worked examples, so read it
before writing SQL rather than guessing table or column names.

- Answer questions about notes with `query` alone. Most requests never need an edit.
- Ask for the columns you need and let the row cap stand. Narrow the query rather
  than raising `limit` when a result is truncated.
- Quote what a note says when you answer, and name the note's path so the user
  can find it.

## Change a note: `open`, then `apply`

1. `open` the file first, even if `query` already showed you its text. It returns
   each line as `LINE:HASH|TEXT` and a `sha`.
2. Make the smallest edit that does the job: `set_line`, `insert_after`,
   `replace_lines` or `replace` against anchors from `open`. Rewrite a whole file
   with `put` only when the user asked for a rewrite.
3. Pass the `sha` from `open` as `base`. It is what stops you overwriting an edit
   the user made on another device while you were working.
4. If `apply` refuses because the file changed, it returns fresh anchors and the
   current `sha`. Re-read what changed, redo the edit against them, and tell the
   user their note had moved on.

A batch is one transaction of at most 100 operations. Split larger changes
across several calls.

## Ask before destroying anything

`delete`, `rename`, a whole-file `put` over an existing note, and `put` with
`force: true` can lose the user's writing. Before sending any of them, say which
files will be affected and wait for the user to agree. Never use `force` unless
the user has said to discard what is there.

`rename` rewrites links to the moved note in the same transaction, so do not
edit those links by hand afterwards.

## When a tool is refused

- **A read-only connection** answers `apply` with a refusal naming a read-write
  token. Tell the user; do not try to reach the change another way.
- **A sign-in prompt or an authorisation error** means the connection to Ctrl
  Notes needs the user to sign in again from their agent's MCP settings.
- **A query refusal** names why, such as a scan budget or an unsupported
  construct. Rewrite the query from the reason given.
