# `xmcfiles`

`xmcinter.xmcfiles` contains the main readers for XMC run products. Most
notebook workflows start here.

```python
import xmcinter.xmcfiles as xf
```

## `merge_output()`

```python
xmcinter.xmcfiles.merge_output(
    runpath="./",
    filetype="deconvolution",
    save=True,
    sep="\t",
    itmin=0,
    itmax=None,
)
```

**Purpose**  
Read many numbered XMC text output files and merge them into one Pandas
`DataFrame`.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | `"./"` | Directory containing XMC output files. |
| `filetype` | `"deconvolution"` | File prefix to merge. Common values are `"deconvolution"`, `"statistic"`, `"sigma"`, `"mean"`, and `"changed"`. |
| `save` | `True` | Write `<filetype>_merged.txt` into `runpath`. Use `False` for in-memory notebook work. |
| `sep` | `"\t"` | Separator used when writing the optional merged text file. |
| `itmin` | `0` | Minimum iteration suffix to read, inclusive. |
| `itmax` | `None` | Maximum iteration suffix to read, inclusive. `None` means use all available upper iterations. |

**Returns**  
`pandas.DataFrame`. An `iteration` column is added from the filename suffix.

**Typical workflow**

```python
run = "/path/to/xmc/run/"

df = xf.merge_output(runpath=run, filetype="deconvolution", save=False)
sf = xf.merge_output(runpath=run, filetype="statistic", save=False)
```

**Notes**

- `statistic.*` files are assigned columns:
  `stat1`, `dof`, `oversim`, `nblobs`, `alpha`, `chi2`.
- `deconvolution.*` files are assigned columns only when `parameters.txt` is
  present.
- Returned rows are not guaranteed to be sorted by iteration.

**Example**

```python
df = xf.merge_output(runpath=run, filetype="deconvolution", save=False, itmin=500)
df = df.sort_values("iteration").reset_index(drop=True)
```

**Additional Tips**
You can view the columns of a particular file such as 

```python
df = xf.merge_output(runpath=run, filetype="deconvolution", save=False, itmin=500)
print(list(df.columns))
['stat1', 'dof', 'oversim', 'nblobs', 'alpha', 'chi2', 'iteration']
```


## `read_parnames()`

```python
xmcinter.xmcfiles.read_parnames(runpath)
```

**Purpose**  
Read `parameters.txt` from an XMC run directory and return the names expected
for columns in `deconvolution.*`.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | required | Directory containing `parameters.txt`. |

**Returns**  
List of strings.

**Typical workflow**

```python
parnames = xf.read_parnames(run)
print(parnames)
```

**Notes**

If `parameters.txt` is missing, use the XMC setup or run notes to assign column
names manually before interpreting parameters physically.

**Example**

```python
df = xf.merge_output(runpath=run, filetype="deconvolution", save=False)
df.columns
```

## `read_spectra()`

```python
xmcinter.xmcfiles.read_spectra(
    runpath="../",
    itmin=1,
    itmax=None,
    logbins=False,
    legacy=False,
    average=False,
    bins=0.03,
    datarange=None,
    oversim="auto",
)
```

**Purpose**  
Read `spectrum_*.fits` or MPI-style `spectrum0_*.fits` files and convert them
into histogram tuples suitable for plotting.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | `"../"` | Run directory containing spectrum FITS files. |
| `itmin` | `1` | Minimum spectrum iteration to read. Use `0` with `itmax=0` for the data spectrum. |
| `itmax` | `None` | Maximum spectrum iteration to read. `None` uses the latest available spectrum file. |
| `logbins` | `False` | Use logarithmically spaced histogram bins. |
| `legacy` | `False` | Interpret old-style spectrum filenames where names are iteration/100. |
| `average` | `False` | Append an average model spectrum to the returned list. |
| `bins` | `0.03` | Histogram bin size, bin count, or bin edges. |
| `datarange` | `None` | Optional histogram data range. |
| `oversim` | `"auto"` | Oversimulation factor. `"auto"` reads it from `statistic.*`. |

**Returns**  
List of histogram tuples: `(y, yerrors, yedges)`.

**Typical workflow**

```python
spectra = xf.read_spectra(runpath=run, itmin=100, itmax=600, average=True)
```

**Notes**

This reader expects the FITS table in the HDU layout used by the legacy XMC
outputs. If a modern FITS file stores the table in a different HDU, inspect it
with `astropy.io.fits.open()`.

**Example**

```python
from astropy.io import fits

with fits.open(f"{run}/spectrum_100.fits") as hdul:
    hdul.info()
```

## `fake_deconvolution()`

```python
xmcinter.xmcfiles.fake_deconvolution(df, suffix="99999", runpath="../")
```

**Purpose**  
Write a DataFrame back to a `deconvolution.<suffix>`-style file. This is mainly
used by spectrum-making utilities that need to hand a subset of blobs to legacy
XMC tooling.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `df` | required | Blob DataFrame to write. |
| `suffix` | `"99999"` | Numeric suffix for generated deconvolution-style files. |
| `runpath` | `"../"` | Run directory used for related XMC files and outputs. |

**Returns**  
Writes files; returns no analysis table.

**Typical workflow**

```python
xf.fake_deconvolution(filtered_df, suffix="99999", runpath=run)
```

**Notes**

Use this only when you need to interoperate with external XMC-style tools. It is
not needed for ordinary DataFrame analysis.

## `remove_nans()`

```python
xmcinter.xmcfiles.remove_nans(datatable, filename=None, verbose=1)
```

**Purpose**  
Drop rows containing missing values from a DataFrame and optionally print a
warning.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `datatable` | required | DataFrame to clean. |
| `filename` | `None` | Optional filename for warning messages. |
| `verbose` | `1` | Warning verbosity. |

**Returns**  
The cleaned DataFrame.

**Example**

```python
clean_df = xf.remove_nans(df, filename="deconvolution.500")
```
