# XMCInter

XMCInter is a legacy Python interface for inspecting and post-processing output
from XMC runs. It is not the XMC engine itself. The package is most useful after
an XMC run has produced files such as `deconvolution.*`, `statistic.*`,
`sigma.*`, `mean.*`, `changed.*`, and `spectrum_*.fits`.

The central workflow is:

1. Read many XMC output files into Pandas `DataFrame` objects.
2. Inspect convergence with `statistic.*` files.
3. Filter blobs by iteration and physical parameters.
4. Add derived quantities such as emission measure and blob size.
5. Make diagnostic plots, spectra, and FITS maps.

Most analysis starts with these imports:

```python
import pandas as pd
import numpy as np

import xmcinter.xmcfiles as xf
import xmcinter.wrangle as xw
import xmcinter.xmcmap as xm
import xmcinter.diagnostics as xd
import xmcinter.plots as xplt
import xmcinter.astro_utilities as astro
```

## What This Documentation Covers

This site emphasizes notebook-oriented use by a scientist analyzing an XMC run:

- reading XMC output files,
- building analysis tables,
- filtering blob samples,
- creating temperature and emission maps,
- plotting diagnostics,
- and understanding the helper modules.

The documentation is intentionally practical rather than exhaustive API output.
For a complete grouped list of important public functions, see the
[Function Index](reference/function-index.md).

## Important Legacy Notes

XMCInter was originally written for older Python and older versions of Bokeh,
Pandas, NumPy, SciPy, and Astropy. The modernized package can be installed with
`pip install -e .`, but some plotting routines may still need small compatibility
updates for current Bokeh versions. The core file-reading and DataFrame workflow
is the most stable path for notebook exploration.

Many high-level routines assume that an XMC run directory contains
`parameters.txt`. If that file is missing, deconvolution files can still be read,
but the blob columns may be numeric until you assign names manually.
