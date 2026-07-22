# aai-coding

A modern Python package scaffolded by **fastship**.

## Development

```bash
pip install -e .[dev]
```

## Versioning

Version lives in `aai_coding/__init__.py` as `__version__`.
Bump it with:

```bash
ship-bump --part 2   # patch
ship-bump --part 1   # minor
ship-bump --part 0   # major
```

## Release

1) Ensure your GitHub issues are labeled (`bug`, `enhancement`, `breaking`).
2) Run:

```bash
ship-gh
ship-pypi
```
