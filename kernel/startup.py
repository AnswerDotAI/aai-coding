from fastcore.utils import *
if os.environ.get('CLAUDE_CODE_SESSION_ID'):
    os.environ.setdefault('EXHASH_JOURNAL', f"/tmp/exhash-journal/{os.environ['CLAUDE_CODE_SESSION_ID']}")
    os.environ.setdefault('EXHASH_AUTHOR', os.environ.get('JUPYGATE_AGENT', 'main'))
elif os.environ.get('JUPYGATE_LAUNCHER') == 'mcp':
    os.environ.setdefault('EXHASH_JOURNAL', '/tmp/exhash-journal/mcp')
    os.environ.setdefault('EXHASH_AUTHOR', os.environ.get('JUPYGATE_AGENT') or os.environ['JUPYGATE_KERNEL_ID'])
# chkstyle: off
from pyskills import list_pyskills, doc, xdir, info_md
from fastcore.editskill import *
from aidialog.dlgskill import *
from exhash.skill import *
from rgapi.skill import *
import clikernel.skill as clik, pyskills.skill as pysk, fastcore.editskill as edsk
import aidialog.dlgskill as dsk, exhash.skill as exh, rgapi.skill as rgsk
import aai_coding.coding_patterns as acp
# chkstyle: on
print(r'''Kernel imports are loaded, including rg/fd/ls from rgapi. If the doc() output for these modules isn't visible in your context, read it now in parallel (separate cells):
doc(clik, pysk)
doc(edsk)
doc(dsk)
doc(exh)
doc(rgsk)
doc(acp)
list_pyskills()''')
