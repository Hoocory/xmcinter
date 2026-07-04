# `diagnostics`

`xmcinter.diagnostics` provides high-level routines that combine several lower
level functions into common XMC run checks.

```python
import xmcinter.diagnostics as xd
```

## `check()`

```python
xmcinter.diagnostics.check(
    runpath="./",
    outpath="./",
    itmin=0,
    itmax=None,
    kTthresh=None,
    cint=False,
    display=False,
    init_file=None,
    skipspectrum=False,
    legacy=False,
)
```

**Purpose**  
Run a broad diagnostic pass over an XMC run. It checks convergence, reads and
cleans blobs, creates plots, and makes a basic norm map.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | `"./"` | Directory containing XMC output files. |
| `outpath` | `"./"` | Directory/prefix for generated plots and maps. |
| `itmin` | `0` | Minimum iteration to use. |
| `itmax` | `None` | Maximum iteration to use; `None` uses the latest available. |
| `kTthresh` | `None` | Optional minimum `blob_kT` for filtered plots/maps. |
| `cint` | `False` | Pass through to `xmcmap.make_map()` for compiled Gaussian integration. |
| `display` | `False` | Show Bokeh figures immediately. |
| `init_file` | `None` | Optional object-specific initialization module. |
| `skipspectrum` | `False` | Skip spectrum plotting when `True`. |
| `legacy` | `False` | Use legacy spectrum filename convention. |

**Returns**  
Tuple `(dfall, sf)`:

- `dfall`: cleaned blob `DataFrame`.
- `sf`: statistic `DataFrame` with reduced chi-square.

**Typical workflow**

```python
dfall, sf = xd.check(
    runpath=run,
    outpath="analysis",
    itmin=500,
    skipspectrum=True,
    display=False,
    cint=False,
)
```

**Notes**

- This is a convenience wrapper, not a no-output function. It writes diagnostic
  HTML/FITS files.
- It assumes deconvolution columns have scientific names such as `blob_phi`,
  `blob_psi`, `blob_kT`, and `blob_norm`.
- On current Bokeh versions, some plotting steps may require compatibility
  updates.

## `clean()`

```python
xmcinter.diagnostics.clean(
    runpath="./",
    itmin=0,
    itmax=None,
    distance=8.0,
)
```

**Purpose**  
Merge/read deconvolution output, filter iterations, and add derived blob
quantities.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | `"./"` | Run directory or a previously merged DataFrame. |
| `itmin` | `0` | Minimum iteration to keep. |
| `itmax` | `None` | Maximum iteration to keep; `None` uses the maximum in the table. |
| `distance` | `8.0` | Object distance in kpc, used to convert norm to emission measure. |

**Returns**  
Filtered and augmented blob `DataFrame`.

**Typical workflow**

```python
df = xd.clean(runpath=run, itmin=500, distance=3.3)
```

**Derived columns**

Depending on available inputs, `clean()` can add:

- `blob_sigma` from `blob_lnsigma`,
- `blob_tau` from `blob_logtau`,
- `blob_em` from `blob_norm`,
- `blob_volume`,
- `blob_numberdensity`,
- `blob_mass2`.

**Notes**

`clean()` writes a `deconvolution_merged_iter<itmin>-<itmax>.txt` file in the
current working directory. For a strictly in-memory workflow, use
`xmcfiles.merge_output()` and add derived columns in the notebook.

**Small in-memory alternative**

```python
import numpy as np
import xmcinter.xmcfiles as xf
import xmcinter.wrangle as xw

df = xf.merge_output(runpath=run, filetype="deconvolution", save=False)
df = xw.filterblobs(df, "iteration", minvals=500)
df["blob_sigma"] = np.exp(df["blob_lnsigma"])
```
