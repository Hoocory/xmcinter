# `wrangle`

`xmcinter.wrangle` contains DataFrame filtering, weighted statistics, histogram
helpers, and a few spectrum/subset utilities.

```python
import xmcinter.wrangle as xw
```

## `filterblobs()`

```python
xmcinter.wrangle.filterblobs(
    inframe,
    colnames,
    minvals=None,
    maxvals=None,
    logic="and",
)
```

**Purpose**  
Filter a blob DataFrame by one or more parameter ranges.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `inframe` | required | Input `pandas.DataFrame`. |
| `colnames` | required | Column name or list of column names. |
| `minvals` | `None` | Minimum value or list of minimum values to keep. |
| `maxvals` | `None` | Maximum value or list of maximum values to keep. |
| `logic` | `"and"` | `"and"` requires all criteria; `"or"` keeps rows matching any criterion. |

**Returns**  
Filtered `pandas.DataFrame`.

**Typical workflow**

```python
df = xw.filterblobs(df, "iteration", minvals=500)
hot = xw.filterblobs(df, "blob_kT", minvals=2.0, maxvals=8.0)
```

**Example**

```python
subset = xw.filterblobs(
    df,
    ["blob_kT", "blob_norm"],
    minvals=[2.0, None],
    maxvals=[8.0, 1e-4],
)
```

## `simplefilterblobs()`

```python
xmcinter.wrangle.simplefilterblobs(
    inframe,
    colname,
    minval=None,
    maxval=None,
    quiet=False,
)
```

**Purpose**  
Single-column helper used by `filterblobs()`.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `inframe` | required | Input DataFrame. |
| `colname` | required | Column to filter. |
| `minval` | `None` | Inclusive lower bound. `None` uses the column minimum. |
| `maxval` | `None` | Inclusive upper bound. `None` uses the column maximum. |
| `quiet` | `False` | Suppress filter warnings when `True`. |

**Returns**  
Filtered DataFrame.

**Typical workflow**  
Prefer `filterblobs()` unless you specifically need the simpler helper.

```python
cool = xw.simplefilterblobs(df, "blob_kT", maxval=1.0)
```

## `filtercircle()`

```python
xmcinter.wrangle.filtercircle(
    inframe,
    x="blob_phi",
    y="blob_psi",
    r="blob_sigma",
    r0=None,
    x0=-60.0,
    y0=80.0,
    logic="exclude",
    fraction=True,
    regname="circle",
    use_ctypes=True,
    parallel=False,
    nproc=3,
)
```

**Purpose**  
Filter blobs by a circular region in the XMC coordinate plane.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `inframe` | required | Blob DataFrame. |
| `x` | `"blob_phi"` | X-coordinate column. |
| `y` | `"blob_psi"` | Y-coordinate column. |
| `r` | `"blob_sigma"` | Blob size column or scalar radius. |
| `r0` | `None` | Circular region radius. |
| `x0` | `-60.0` | Circular region center x-coordinate. |
| `y0` | `80.0` | Circular region center y-coordinate. |
| `logic` | `"exclude"` | `"exclude"` removes the region; `"include"` keeps the region. |
| `fraction` | `True` | Add fractional contribution columns instead of only dropping rows. |
| `regname` | `"circle"` | Prefix for generated region-fraction columns. |
| `use_ctypes` | `True` | Use compiled Gaussian helper where available. |
| `parallel` | `False` | Use multiprocessing for region fraction calculations. |
| `nproc` | `3` | Number of processes when `parallel=True`. |

**Returns**  
Filtered DataFrame or a DataFrame with region-fraction columns.

**Example**

```python
inside = xw.filtercircle(
    df,
    x="blob_phi",
    y="blob_psi",
    r="blob_sigma",
    x0=0.0,
    y0=0.0,
    r0=60.0,
    logic="include",
)
```

## Weighted Statistics

### `weighted_median()`

```python
xmcinter.wrangle.weighted_median(data, weights=None)
```

**Purpose**  
Compute a weighted median.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `data` | required | Array-like values. |
| `weights` | `None` | Optional weights. If `None`, behaves like an unweighted median. |

**Returns**  
Scalar or array, depending on input.

**Example**

```python
median_kT = xw.weighted_median(df["blob_kT"], weights=df["blob_norm"])
```

### `weighted_std()`

```python
xmcinter.wrangle.weighted_std(data, weights=None, ddof=1.0)
```

**Purpose**  
Compute a weighted standard deviation.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `data` | required | Array-like values. |
| `weights` | `None` | Optional weights. |
| `ddof` | `1.0` | Delta degrees of freedom for variance normalization. |

**Example**

```python
sigma_kT = xw.weighted_std(df["blob_kT"], weights=df["blob_norm"])
```

### `weighted_modes()`

```python
xmcinter.wrangle.weighted_modes(data, weights=None, bins=75, logbins=False)
```

**Purpose**  
Estimate modes from a weighted histogram.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `data` | required | Array-like values. |
| `weights` | `None` | Optional weights. |
| `bins` | `75` | Histogram bin count or bin specification. |
| `logbins` | `False` | Use logarithmic bins. |

**Example**

```python
modes = xw.weighted_modes(df["blob_kT"], weights=df["blob_norm"], bins=75)
```

### `credible_region()`

```python
xmcinter.wrangle.credible_region(data, weights=None, frac=0.9, method="HPD")
```

**Purpose**  
Calculate a Bayesian credible region from a posterior sample.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `data` | required | Posterior samples. |
| `weights` | `None` | Optional sample weights. |
| `frac` | `0.9` | Credible-region fraction. |
| `method` | `"HPD"` | Credible-region method. |

**Example**

```python
region = xw.credible_region(df["blob_kT"], weights=df["blob_norm"], frac=0.9)
```

## Histogram Helpers

### `make_histogram()`

```python
xmcinter.wrangle.make_histogram(
    dataseries,
    weights=None,
    bins=50,
    logbins=False,
    datarange=None,
    density=False,
    iterations=None,
    centers=False,
    normalize=False,
)
```

**Purpose**  
Create a histogram with optional weights, log bins, and iteration-based error
bars.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `dataseries` | required | Data values to histogram. |
| `weights` | `None` | Optional weights for each value. |
| `bins` | `50` | Bin count, bin edges, or NumPy-compatible bin spec. |
| `logbins` | `False` | Use logarithmically spaced bins. |
| `datarange` | `None` | Optional histogram range. |
| `density` | `False` | Return density instead of counts. |
| `iterations` | `None` | Optional per-row iterations for error estimates. |
| `centers` | `False` | Return bin centers instead of edges where supported. |
| `normalize` | `False` | Normalize histogram values. |

**Returns**  
Usually a tuple of histogram values, errors, and bin edges.

**Example**

```python
y, yerr, edges = xw.make_histogram(
    df["blob_kT"],
    weights=df["blob_norm"],
    bins=50,
)
```

### `normalize_histogram()`

```python
xmcinter.wrangle.normalize_histogram(histy, yerrors=None)
```

**Purpose**  
Normalize histogram values and optionally their errors.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `histy` | required | Histogram y values. |
| `yerrors` | `None` | Optional histogram errors to scale with `histy`. |

**Example**

```python
y_norm, yerr_norm = xw.normalize_histogram(y, yerr)
```

### `iter_err()`

```python
xmcinter.wrangle.iter_err(df, param, function, weights=None, *args, **kwargs)
```

**Purpose**  
Estimate variation in a statistic across iterations.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `df` | required | DataFrame with an `iteration` column. |
| `param` | required | Parameter column to summarize. |
| `function` | required | Statistic function to apply per iteration. |
| `weights` | `None` | Optional weight column or values. |
| `*args`, `**kwargs` | none | Extra arguments passed to `function`. |

**Example**

```python
err = xw.iter_err(df, "blob_kT", xw.weighted_median, weights="blob_norm")
```

## Spectral Subset Helpers

### `make_spectrum()`

```python
xmcinter.wrangle.make_spectrum(
    df,
    runpath="../",
    suffix="99999",
    oversim="auto",
    bins=0.03,
    xlog=False,
    logbins=None,
    datarange=None,
    fixed_nH=None,
)
```

**Purpose**  
Create a spectrum from a selected set of blobs. This function can call legacy
XMC-style file paths and is more specialized than ordinary plotting.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `df` | required | Blob subset DataFrame. |
| `runpath` | `"../"` | XMC run directory. |
| `suffix` | `"99999"` | Suffix for temporary/generated deconvolution-style files. |
| `oversim` | `"auto"` | Oversimulation factor or `"auto"` to infer it. |
| `bins` | `0.03` | Spectrum histogram bins or bin size. |
| `xlog` | `False` | Use logarithmic x-axis interpretation. |
| `logbins` | `None` | Use logarithmic bins; `None` follows `xlog`. |
| `datarange` | `None` | Optional histogram range. |
| `fixed_nH` | `None` | Optional fixed absorption column for spectrum generation. |

**Example**

```python
spec = xw.make_spectrum(subset, runpath=run, suffix="99999", bins=0.03)
```

### `normclean()`

```python
xmcinter.wrangle.normclean(
    df,
    nHcol="blob_nH",
    kTcol="blob_kT",
    normcol="blob_norm",
    itercol="iteration",
    normthreshs=None,
    parallel=False,
    nproc=4,
)
```

**Purpose**  
Remove low-temperature/high-absorption blobs using normalization criteria. This
is an advanced cleaning helper for specific models that include `nH`, `kT`, and
norm columns.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `df` | required | Blob DataFrame. |
| `nHcol` | `"blob_nH"` | Absorption column. |
| `kTcol` | `"blob_kT"` | Temperature column. |
| `normcol` | `"blob_norm"` | Normalization column. |
| `itercol` | `"iteration"` | Iteration column. |
| `normthreshs` | `None` | Threshold configuration for norm cleaning. |
| `parallel` | `False` | Use multiprocessing. |
| `nproc` | `4` | Number of processes when `parallel=True`. |

**Example**

```python
cleaned = xw.normclean(df, nHcol="blob_nH", kTcol="blob_kT", normcol="blob_norm")
```

## Line Emission Helpers

### `line_emissivities()` and `blob_line_photons()`

```python
xmcinter.wrangle.line_emissivities(kT, tolerance=0.05, **fetchargs)
xmcinter.wrangle.blob_line_photons(kT, volume, time=None, tolerance=0.01, **fetchargs)
```

**Purpose**  
Estimate line emissivity or line photon output for gas at a given temperature.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `kT` | required | Gas temperature in keV. |
| `volume` | required for `blob_line_photons()` | Blob volume. |
| `time` | `None` | Optional exposure/time scale for photon estimate. |
| `tolerance` | `0.05` / `0.01` | Temperature matching tolerance. |
| `**fetchargs` | none | Extra line-list filters passed through to line-fetching helpers. |

**Example**

```python
lines = xw.line_emissivities(kT=1.0)
photons = xw.blob_line_photons(kT=1.0, volume=1e55)
```
