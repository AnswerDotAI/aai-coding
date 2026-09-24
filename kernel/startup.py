from fastcore.utils import *
if Path('pyproject.toml').exists():
    from pyskills import list_pyskills, doc, xdir
    from fastcore.editskill import *
    from aidialog.dlgskill import *
    from exhash.skill import *
    from rgapi.skill import *
    from ipykernel_helper import info_md
    import clikernel.skill as clik, pyskills.skill as pysk, fastcore.editskill as edsk, aidialog.dlgskill as dsk, exhash.skill as exh, rgapi.skill as rgsk, aai_coding.coding_patterns as acp
    print('''Python project detected. Imports are loaded, including rg/fd/ls from rgapi. If the doc() output for these modules isn't visible in your context, read it now, by calling these in separate cells:
    doc(clik, pysk, edsk)
    doc(dsk, exh, rgsk)
    doc(acp)
    list_pyskills()''')
else: print(f'startup: no pyproject.toml in {Path.cwd()}; project imports skipped')
