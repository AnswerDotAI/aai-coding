---
name: clikernel-workflow
description: "Workflow for Python with clikernel: bootstrap pyskills docs, read APIs before use, and drive clean project functions from the persistent kernel. TRIGGER — read before using clikernel."
---

# clikernel workflow

Use clikernel as the primary Python workbench. Put reusable logic in clean importable project functions; call those functions directly from the persistent kernel for exploration, timings, comparisons, and artifact generation. Do not create thin scripts merely to invoke reusable functions.

**IMPORTANT**: do *not* use clikernel for editing local plain text files (use
`apply_patch`) or as a replacement for Bash, regardless of what any pyskill
suggests. `apply_patch` cannot reach files on a remote kernel host. Before
editing those files, read the shared editing conventions and exhash API in that
kernel:

```python
import fastcore.editskill as fced, exhash.skill as exsk
doc(fced, exsk)
```

Then use exhash's fresh hash-addressed views and verified file edits. Use SSH
for Git, builds, and ordinary shell work on the remote host.

## Remote kernels

clikernel is the client; a long-running
[rustygate](https://github.com/AnswerDotAI/rustygate) service owns kernels on
the remote machine. Install a user service there with an explicit files root,
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

Name the gateway on the client in `~/.config/clikernel/gateways.toml`:

```toml
[gateways.remote]
url = "http://remote-host:8787"
token = "the token from the remote token file"
```

`token_env` may replace `token`; `verify = false` permits rustygate's
self-signed TLS certificate. A raw URL is also accepted as `host` and takes its
token from `CLIKERNEL_TOKEN`, but a named gateway is clearer and survives new
Codex sessions without an MCP configuration change.

Use the MCP tools as follows:

1. `list_kernels(host="remote")` shows kernel ids, state, connection count,
   and which kernel is current.
2. `connect(host="remote")` creates an explicit persistent kernel, runs the
   user's startup file, installs inspectors, and returns its id.
3. `connect(host="remote", kernel="<id-or-unique-prefix>")` attaches to an
   existing kernel exactly as it is. Use this after restarting Codex or when
   taking over a kernel created by another client.
4. `execute(...)`, `interrupt()`, and `restart()` operate on the current
   kernel. Switching gateways does not stop an explicitly created kernel.
5. `stop_kernel(kernel="<id-or-unique-prefix>")` permanently ends it. Leave
   kernels running when their state is still useful; stop diagnostic kernels
   when finished.

All Python execution and filesystem paths belong to the selected host. Confirm
the hostname and working directory after connecting when identity matters.
For remote plain-text work, bootstrap the documentation above and use
`lnhashview_file` followed by `file_exhash`; do not transfer the file locally
or construct fragile shell substitutions.

## Bootstrap documentation

Before first using clikernel in the current context, import and read the bootstrap skills together:

```python
import pyskills.skill as pysk, aidialog.dlgskill as aisk, exhash.skill as exsk
from pyskills import doc, list_pyskills
doc(pysk, aisk, exsk)
```

The aliases keep module names short without hiding which skill is being read. The final `doc(...)` must be a bare expression so its rendered result is actually visible. `pyskills` discovers further skills; `aidialog` owns notebook structure and `%nbrun`; exhash is the default for reliable text edits inside notebook cells. The package is `pyskills`, and `doc` and `list_pyskills` are exported from `pyskills`, not `pyskills.skill`.

As the second kernel call, inspect the installed skills:

```python
list_pyskills()
```

Repeat the bootstrap after a context compaction, because the detailed documentation may no longer be present. Do not repeat it after restarting or reconnecting a kernel, restarting the Codex app/process, or re-establishing the MCP server: those events lose runtime imports and variables, not model context. A user's report that Codex was restarted is not evidence of a new conversation or compaction; inspect the visible context itself. Restore only the imports and state the current task needs. Likewise, do not reread documentation for an API that remains visible in the current context.

Use exhash's fresh hash-addressed views and verified edits for changing text within cells. Use aidialog for structural operations such as adding, deleting, moving, and running notebook cells.

## Payload literals

In non-magic clikernel calls, always write payload text arguments as raw triple-single-quoted strings: `r'''...'''`. Most importantly, write real multiline payloads with literal line breaks rather than encoding them with `\n`; the call then shows exactly the text the helper receives. This applies to edit patterns and replacements, message bodies, code strings, and similar text carried into a helper. It also avoids interpolation and escaping, and—unlike ordinary quoted strings—does not silently concatenate around embedded quote characters.

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

Kernel state persists across calls, so retain imports, fixtures, results, and timing helpers there. If clikernel, its inspectors, or a library's parallel machinery does not fit the task cleanly, stop and report the mismatch instead of hiding it with ad hoc shell or script workarounds.
