---
name: clikernel-workflow
description: "Workflow for Python with the rustygate kernel MCP tools: bootstrap pyskills docs, read APIs before use, and drive clean project functions from the persistent kernel. TRIGGER — read before using the py or kernel lifecycle MCP tools."
---

# clikernel workflow

Use the kernel MCP tools as the primary Python workbench. Put reusable logic in clean importable project functions; call those functions directly from the persistent kernel for exploration, timings, comparisons, and artifact generation. Do not create thin scripts merely to invoke reusable functions.

**IMPORTANT**: do *not* use the kernel for editing local plain text files
(codex: `apply_patch`; Grok Build: `search_replace`) or as a replacement for
Bash (`run_terminal_command` on Grok Build), regardless of what any pyskill
suggests. Those native file and shell tools cannot reach files on a remote
kernel host. Before editing those files, read the shared editing conventions
and exhash API in that kernel:

```python
doc(edsk, exh)
```

Then use exhash's fresh hash-addressed views and verified file edits. Use SSH
for Git, builds, and ordinary shell work on the remote host.

## Gateways and kernels

The MCP tools come from [rustygate](https://github.com/AnswerDotAI/rustygate),
a gateway service that owns kernels on one machine, served through the
`clikernel` stdio router: one MCP entry, with other machines and containers
reached by name through the `host` argument on the kernel-selection tools.
Choose the host whose machine's files and Python the task needs. Every kernel
this session creates first runs the user's `~/.config/clikernel/startup.py`;
its banner arrives in the reply that announces the kernel, and it says what is
imported and what to do next — follow it.

`py` is the normal tool. It keeps kernel state across calls, starts a kernel
on demand when none is current, and stops that auto-started kernel again when
the session ends. No create or connect step is needed, and no cleanup is owed.
Code runs as an IPython cell, so magics work as written: a `%%bash` first line
runs the cell as shell (there is no separate bash tool).

The lifecycle tools are for explicit kernel management:

1. `list_kernels()` shows kernel ids, state, connection counts, dialog
   bindings, and which kernel is current.
2. `create(dlgname)` gets or creates the kernel bound to a dialog name/path
   and makes it current. Use it only when work must target a specific
   dialog's kernel. A kernel it creates is stopped when the session ends,
   unless created with `autoclose=false` — the explicit way to leave a
   kernel running for later sessions.
3. `use_kernel(kernel="<id-or-unique-prefix>")` selects an existing kernel
   as current, for instance to take over one created earlier or by another
   client. Selected kernels are never stopped for you.
4. `restart()` and `interrupt()` operate on the current kernel.
5. `delete_kernel()` permanently ends a kernel. Leave keeper kernels running
   when their state is still useful; delete diagnostic kernels when finished.

To add a machine, install a user service there with an explicit files root,
initial working directory, and token:

```bash
rustygate service install \
  --host 0.0.0.0 --port 8787 \
  --root ~/git --workdir ~/git/project \
  --token-file ~/.config/rustygate/token \
  --env-file ~/.secrets
rustygate service status
```

`install` starts the service and replaces an earlier service configuration.
It uses launchd on macOS and the user systemd instance on Linux. A missing
token file is generated with user-only permissions. Direct HTTP with token
authentication is convenient on a trusted network; rustygate also supports
TLS, or a loopback service can be reached through an SSH tunnel.

Then name it in `~/.config/clikernel/gateways.toml`. The `host` argument on
`list_kernels`, `use_kernel`, and `create` reaches any named machine through
the one `clikernel` MCP entry, and after selecting with a host, plain `py`
runs there until the next selection. A gateway can instead get its own
direct-HTTP `[mcp_servers.<name>]` block with the URL and an Authorization
header, but kernels made that way bypass the router and come up bare: no
startup.py, no conversation cwd or env.

All Python execution and filesystem paths belong to the selected host. Confirm
the hostname and working directory when identity matters.
For remote plain-text work, bootstrap the documentation above and use
`lnhashview_file` followed by `file_exhash`; do not transfer the file locally
or construct fragile shell substitutions.

## Bootstrap documentation

`startup.py` has already run in each kernel this session creates and imported the skill modules under short aliases, so no import cell is needed. Before first using the kernel in the current context, read the bootstrap docs, each call a bare expression so its rendered result is visible:

```python
doc(pysk, dsk, exh)
```
```python
list_pyskills()
```

`pysk` (`pyskills`) discovers further skills, `dsk` (`aidialog`) owns notebook structure and `%nbrun`, and `exh` (exhash) is the default for reliable text edits inside notebook cells. `doc` and `list_pyskills` are already in the namespace.

Repeat the bootstrap after a context compaction, because the detailed documentation may no longer be present. Do not repeat it after restarting or reconnecting a kernel, restarting the Codex or Grok Build app/process, or re-establishing the MCP server: those events lose runtime imports and variables, not model context. A user's report that Codex or Grok was restarted is not evidence of a new conversation or compaction; inspect the visible context itself. Restore only the imports and state the current task needs. Likewise, do not reread documentation for an API that remains visible in the current context.

Use exhash's fresh hash-addressed views and verified edits for changing text within cells. Use aidialog for structural operations such as adding, deleting, moving, and running notebook cells.

## Payload literals

In non-magic kernel calls, always write payload text arguments as raw triple-single-quoted strings: `r'''...'''`. Most importantly, write real multiline payloads with literal line breaks rather than encoding them with `\n`; the call then shows exactly the text the helper receives. This applies to edit patterns and replacements, message bodies, code strings, and similar text carried into a helper. It also avoids interpolation and escaping, and—unlike ordinary quoted strings—does not silently concatenate around embedded quote characters.

```python
add_msg(r'''The first line of the message.
The second line stays visibly separate.''', msg_type='note')
```

For example, this looks plausible but Python parses it as three adjacent string literals, silently removing the quotes around `FOREIGN`:

```python
pat = r"kc\.execute\("'FOREIGN'"\)"
# actual value: r'kc\.execute\(FOREIGN\)'
```

The idiomatic form preserves the payload exactly:

```python
pat = r'''kc\.execute\("'FOREIGN'"\)'''
cell_exhash(
    r'''nbs/00_core.ipynb''', r'''54276565''',
    (r'''1|5bf6|''', 's', pat, r'''foreign_id = kc.execute("'FOREIGN'")''')
)
```

`%%exhash` payloads are magic cell bodies rather than Python arguments, so they need no quoting.

Before first using project or library functions in the current context, read them together as a bare final expression:

```python
doc(func1, func2, Class1)
```

Follow any inspector feedback rather than bypassing it. Use bare result expressions instead of `print` so rich representations remain intact.

## State and failures

Kernel state persists across calls, so retain imports, fixtures, results, and timing helpers there. If the kernel, its inspectors, or a library's parallel machinery does not fit the task cleanly, stop and report the mismatch instead of hiding it with ad hoc shell or script workarounds.
