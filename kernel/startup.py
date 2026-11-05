from fastcore.utils import *
if os.environ.get('CLAUDE_CODE_SESSION_ID'):
    os.environ.setdefault('EXHASH_JOURNAL', f"/tmp/exhash-journal/{os.environ['CLAUDE_CODE_SESSION_ID']}")
    os.environ.setdefault('EXHASH_AUTHOR', os.environ.get('RUSTYGATE_AGENT', 'main'))
elif os.environ.get('RUSTYGATE_LAUNCHER') == 'mcp':
    os.environ.setdefault('EXHASH_JOURNAL', '/tmp/exhash-journal/mcp')
    os.environ.setdefault('EXHASH_AUTHOR', os.environ.get('RUSTYGATE_AGENT') or os.environ['RUSTYGATE_KERNEL_ID'])
from pyskills import list_pyskills, doc, xdir, info_md
from fastcore.editskill import *
from aidialog.dlgskill import *
from exhash.skill import *
from rgapi.skill import *
import clikernel.skill as clik, pyskills.skill as pysk, fastcore.editskill as edsk
import aidialog.dlgskill as dsk, exhash.skill as exh, rgapi.skill as rgsk
import aai_coding.coding_patterns as acp
print(r'''Kernel imports are loaded, including rg/fd/ls from rgapi. If the doc() output for these modules isn't visible in your context, read it now, by calling these in separate cells:
doc(clik, pysk, edsk)
doc(dsk, exh, rgsk)
doc(acp)
list_pyskills()''')
