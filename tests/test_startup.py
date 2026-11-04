import runpy, pytest
from pathlib import Path


@pytest.mark.parametrize('project', [False, True])
def test_startup_tools_in_any_directory(tmp_path, monkeypatch, project):
    startup = Path(__file__).parents[1]/'kernel/startup.py'
    if project: (tmp_path/'pyproject.toml').touch()
    monkeypatch.chdir(tmp_path)
    ns = runpy.run_path(startup)
    assert all(callable(ns[k]) for k in ('doc', 'list_pyskills', 'open_doc', 'file_exhash', 'rg'))
    assert all(k in ns for k in ('clik', 'pysk', 'edsk', 'dsk', 'exh', 'rgsk', 'acp'))
