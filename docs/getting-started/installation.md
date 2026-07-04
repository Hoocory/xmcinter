# Installation

XMCInter now uses a modern editable package layout. Install it from the project
root with `pip`.

```bash
git clone <repository-url> xmcinter
cd xmcinter
pip install -e .
```

The editable install lets notebooks import the package while you continue to
inspect or improve the documentation and source tree.

## Verify the Install

Run Python from any directory and import a core module:

```python
import xmcinter.xmcfiles as xf

print(xf.__file__)
```

The printed path should point into the cloned `xmcinter` checkout.

## Optional Documentation Dependencies

The documentation site uses MkDocs and the Material theme:

```bash
pip install mkdocs mkdocs-material
```

Then serve the documentation locally from the project root:

```bash
mkdocs serve
```

## Optional Map Acceleration

`xmcinter.xmcmap.make_map()` can use a compiled `gaussian.so` helper when
called with `cint=True`. If the checked-in shared library is incompatible with
your system, rebuild it locally:

```bash
cd src/xmcinter
clang -shared -fPIC -o gaussian.so gaussian.c
```

For the most portable notebook workflow, pass `cint=False` to `make_map()`.
