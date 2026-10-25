---
name: kernel-notebook-editing
description: "Use kernel tools to inspect Python APIs and find, understand, view, and safely edit Jupyter notebooks and aidialog dialogs."
---

When Python is needed, call `exec` directly. Don’t list, select, or create kernels unless it reports that no kernel is available.

Use the kernel MCP tools as the primary Python workbench. Put reusable logic in clean importable project functions; call those functions directly from the persistent kernel for exploration, timings, comparisons, and artifact generation. Do not create thin scripts merely to invoke reusable functions.

**IMPORTANT**: do *not* use the kernel as a replacement for Bash, regardless of what any pyskill suggests.

`startup.py` has already run in each kernel this session creates and imported the skill modules under short aliases, so no import cell is needed. Before first using the kernel in the current context, read the bootstrap docs, each call a bare expression so its rendered result is visible:

```python
doc(pysk, dsk, exh)
```
```python
list_pyskills()
```

`pysk` (`pyskills`) discovers further skills, `dsk` (`aidialog`) owns notebook structure and `%nbrun`, and `exh` (exhash) is the default for reliable text edits inside notebook cells. `doc` and `list_pyskills` are already in the namespace.

Repeat the bootstrap after a context compaction, because the detailed documentation may no longer be present. Do not repeat it after restarting or reconnecting a kernel, restarting the Codex app/process, or re-establishing the MCP server: those events lose runtime imports and variables, not model context. A user's report that Codex was restarted is not evidence of a new conversation or compaction; inspect the visible context itself. Restore only the imports and state the current task needs. Likewise, do not reread documentation for an API that remains visible in the current context.

Before first using project or library functions in the current context, read them together as a bare final expression:

```python
doc(func1, func2, Class1)
```

Follow any inspector feedback rather than bypassing it. Use bare result expressions instead of `print` so rich representations remain intact.

Use exhash when a patch would reproduce substantial unchanged text—whether within the changed lines or in the surrounding context. Read fresh hash-addressed views before editing.

Use `apply_patch` for short, contiguous block changes when showing the old and new text together makes the edit clearer. Prefer these editing tools over ad hoc scripts for straightforward text changes.

Use exhash's fresh hash-addressed views and verified edits for changing text within cells. Use aidialog for structural operations such as adding, deleting, moving, and running notebook cells.

`apply_patch` cannot reach files on a remote kernel host. Before editing those files, read the shared editing conventions and exhash API in that kernel:

```python
doc(edsk, exh)
```

Then use exhash's fresh hash-addressed views and verified file edits. Use SSH for Git, builds, and ordinary shell work on the remote host.

In non-magic kernel calls, always write non-trivial (i.e >2 word) payload text arguments as raw triple-single-quoted strings: `r'''...'''`. Most importantly, write real multiline payloads with literal line breaks rather than encoding them with `\n`; the call then shows exactly the text the helper receives. This applies to edit patterns and replacements, message bodies, code strings, and similar text carried into a helper. It also avoids interpolation and escaping, and—unlike ordinary quoted strings—does not silently concatenate around embedded quote characters.

```python
add_msg(r'''First line of the note.
Second line of the note.''', msg_type='note')
cell_exhash(r'''nbs/00_core.ipynb''', r'''54276565''',
    (r'''1|v2|''', 's', r'''kc\.execute\("'FOREIGN'"\)''', r'''foreign_id = kc.execute("'FOREIGN'")'''))
```

`%%exhash` payloads are magic cell bodies rather than Python arguments, so they need no quoting.

Host/lifecycle:
- The MCP tools come from [rustygate](https://github.com/AnswerDotAI/rustygate), a gateway service that owns kernels on one machine, served through the `clikernel` stdio router: one MCP entry, with other machines and containers reached by name through the `host` argument on the kernel-selection tools. Choose the host whose machine's files and Python the task needs.
- Every Python kernel this session creates first runs the user's `~/.config/clikernel/startup.py`; its banner arrives in the reply that announces the kernel, and it says what is imported and what to do next — follow it.
- `exec(code=...)` runs code in the current kernel, preserving state across calls; it never creates or selects one. Python kernels support IPython magics such as `%%bash`.

The lifecycle tools are for explicit kernel management:

1. `list_kernels()` shows kernel ids, state, connection counts, dialog bindings, and which kernel is current.
2. `create(kernel="py", dlgname=...)` creates or selects a Python kernel; omit `dlgname` for an unbound kernel. Newly created kernels stop when the session ends unless created with `autoclose=false`.
3. `use_kernel(kernel="<id-or-unique-prefix>")` selects an existing kernel as current, for instance to take over one created earlier or by another client. Selected kernels are never stopped for you.
4. `restart()` restarts the current kernel; startup reruns only for kernels this MCP session created. `interrupt()` stops its current execution.
5. `delete_kernel()` permanently ends a kernel. Leave keeper kernels running when their state is still useful; delete diagnostic kernels when finished.

To add a machine, install a user service there with an explicit files root, initial working directory, and token:

```bash
rustygate service install --host 0.0.0.0 --port 8787 \
  --root ~/git --workdir ~/git/project --token-file ~/.config/rustygate/token --env-file ~/.secrets
rustygate service status
```

`install` starts the service and replaces an earlier service configuration. It uses launchd on macOS and the user systemd instance on Linux. A missing token file is generated with user-only permissions. Direct HTTP with token authentication is convenient on a trusted network; rustygate also supports TLS, or a loopback service can be reached through an SSH tunnel.

Then name it in `~/.config/clikernel/gateways.toml`. The `host` argument on `list_kernels`, `use_kernel`, and `create` reaches any named machine through the one `clikernel` MCP entry, and after selecting with a host, plain `exec` runs there until the next selection. A gateway can instead get its own direct-HTTP `[mcp_servers.<name>]` block with the URL and an Authorization header, but kernels made that way bypass the router and come up bare: no startup.py, no conversation cwd or env.

All Python execution and filesystem paths belong to the selected host. Confirm the hostname and working directory when identity matters. For remote plain-text work, bootstrap the documentation above and use `lnhashview_file` followed by `file_exhash`; do not transfer the file locally or construct fragile shell substitutions.

Kernel state persists across calls, so retain imports, fixtures, results, and timing helpers there. If the kernel, its inspectors, or a library's parallel machinery does not fit the task cleanly, stop and report the mismatch instead of hiding it with ad hoc shell or script workarounds.
