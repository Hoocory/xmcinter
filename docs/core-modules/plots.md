# `plots`

`xmcinter.plots` contains legacy Bokeh plotting helpers for convergence,
histograms, scatter plots, traces, and spectra.

```python
import xmcinter.plots as xplt
```

## Notebook Output

Many functions accept `outfile="notebook"`:

```python
import bokeh.plotting as bplt

bplt.output_notebook()
```

Some plotting calls use older Bokeh APIs. If a Bokeh plot fails, the underlying
DataFrame can usually still be plotted with Pandas or Matplotlib.

## `chi2()`

```python
xmcinter.plots.chi2(
    runpath="./",
    itmin=0,
    itmax=None,
    outfile="chi2_vs_iteration.html",
    display=True,
)
```

**Purpose**  
Read `statistic.*` files, calculate reduced chi-square, and plot chi-square per
degree of freedom versus iteration.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | `"./"` | XMC run directory. |
| `itmin` | `0` | Minimum iteration to plot. |
| `itmax` | `None` | Maximum iteration to plot. |
| `outfile` | `"chi2_vs_iteration.html"` | HTML filename, or `"notebook"` for notebook output. |
| `display` | `True` | Show the Bokeh figure instead of only saving it. |

**Returns**  
Statistic `DataFrame` with a `redchi2` column.

**Example**

```python
sf = xplt.chi2(runpath=run, itmin=500, outfile="notebook")
```

## `trace()`

```python
xmcinter.plots.trace(
    inframe,
    iteration_type="median",
    itercol="iteration",
    weights=None,
    itmin=0,
    itmax=None,
    display=True,
    save=True,
    outfile="trace_plots.html",
    ncols=4,
    height=300,
    width=300,
)
```

**Purpose**  
Plot parameter values or per-iteration summaries as a function of iteration.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `inframe` | required | DataFrame with an iteration column. |
| `iteration_type` | `"median"` | Per-iteration summary: `"median"`, `"average"`, `"stdev"`, `"total"`, or `None`. |
| `itercol` | `"iteration"` | Iteration column name. |
| `weights` | `None` | Optional weight column. |
| `itmin` | `0` | Minimum iteration to plot. |
| `itmax` | `None` | Maximum iteration to plot. |
| `display` | `True` | Show the Bokeh figure. |
| `save` | `True` | Save or emit the Bokeh output. |
| `outfile` | `"trace_plots.html"` | HTML filename, or `"notebook"` for notebook output. |
| `ncols` | `4` | Number of columns in the plot grid. |
| `height` | `300` | Individual plot height in pixels. |
| `width` | `300` | Individual plot width in pixels. |

**Returns**  
Bokeh figure or grid object.

**Example**

```python
fig = xplt.trace(
    df[["iteration", "blob_kT", "blob_norm"]],
    weights=None,
    outfile="notebook",
)
```

## `histogram()` and `histogram_grid()`

```python
xmcinter.plots.histogram(
    dataseries,
    weights=None,
    bins=100,
    save=True,
    display=True,
    height=600,
    median=False,
    mode=False,
    mean=False,
    stdev=False,
    width=800,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    infig=None,
    color="steelblue",
    outfile="histogram.html",
    density=False,
    alpha=None,
    xlog="auto",
    logbins=None,
    legend=None,
    norm=False,
    xmin=None,
    xmax=None,
    iterations=None,
    ymax=None,
    ymin=None,
    scale=1.0,
    ytitle=None,
    ylog=False,
    **kwargs,
)
```

```python
xmcinter.plots.histogram_grid(
    dframes,
    columns=None,
    weights=None,
    bins=100,
    height=300,
    width=400,
    iterations=None,
    display=True,
    ncols=2,
    outfile="histogram_grid.html",
    ymax=None,
    ylog=False,
    colors=["steelblue", "darkolivegreen", "mediumpurple", "darkorange", "firebrick", "gray"],
    xlog="auto",
    median=False,
    mode=False,
    scales=1.0,
    logbins=None,
    alphas=None,
    norm=False,
    legends=None,
    **histargs,
)
```

**Purpose**  
Plot weighted or unweighted posterior distributions.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `dataseries` / `dframes` | required | Input series or DataFrame(s). |
| `columns` | `None` | Columns to include in `histogram_grid()`. |
| `weights` | `None` | Optional weight series, column name, or list of weights. |
| `bins` | `100` | Histogram bins or NumPy-compatible bin spec. |
| `save` | `True` | Save/emit the plot for `histogram()`. |
| `display` | `True` | Show the Bokeh figure. |
| `height`, `width` | `600`, `800` or `300`, `400` | Plot dimensions in pixels. |
| `median`, `mode`, `mean`, `stdev` | `False` | Add summary markers where supported. |
| `tools` | `"pan,wheel_zoom,box_zoom,reset,save"` | Bokeh tools for `histogram()`. |
| `infig` | `None` | Existing Bokeh figure for overplotting. |
| `color`, `colors` | `"steelblue"` / list | Histogram color(s). |
| `outfile` | `"histogram.html"` / `"histogram_grid.html"` | HTML filename, or `"notebook"`. |
| `density` | `False` | Return density-style histogram in `histogram()`. |
| `alpha`, `alphas` | `None` | Fill opacity. |
| `xlog` | `"auto"` | Log-scale x-axis control. |
| `logbins` | `None` | Logarithmic binning control. |
| `legend`, `legends` | `None` | Legend label(s). |
| `norm` | `False` | Normalize histogram height. |
| `xmin`, `xmax`, `ymin`, `ymax` | `None` | Axis limits where supported. |
| `iterations` | `None` | Optional iteration labels for uncertainty estimates. |
| `scale`, `scales` | `1.0` | Scale histogram values. |
| `ytitle` | `None` | Y-axis label for `histogram()`. |
| `ylog` | `False` | Use a log y-axis. |
| `ncols` | `2` | Number of columns in `histogram_grid()`. |
| `**kwargs`, `**histargs` | none | Extra plotting options passed through to lower-level plotting calls. |

**Returns**  
Bokeh figure or list/grid of figures.

**Example**

```python
figs = xplt.histogram_grid(
    df,
    columns=["blob_kT", "blob_norm"],
    weights="blob_norm",
    bins=50,
    outfile="notebook",
)
```

## `scatter()` and `scatter_grid()`

```python
xmcinter.plots.scatter(
    inframe,
    x,
    y,
    sampling=2000,
    agg=None,
    aggcol=None,
    save=True,
    display=True,
    width=600,
    height=600,
    source=None,
    tools=None,
    size=5,
    xlog="auto",
    ylog="auto",
    outfile=None,
    returnfunc=False,
    span=None,
    cscale="eq_hist",
)
```

```python
xmcinter.plots.scatter_grid(
    dframe,
    sampling=1000.0,
    agg=None,
    aggcol=None,
    outfile="scatter_grid.html",
    save=True,
    display=True,
    size=None,
)
```

**Purpose**  
Explore relationships between blob parameters.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `inframe` / `dframe` | required | Blob DataFrame. |
| `x`, `y` | required for `scatter()` | Columns for a single scatter plot. |
| `sampling` | `2000` / `1000.0` | Maximum number of rows to plot. |
| `agg` | `None` | Optional Datashader aggregation mode. |
| `aggcol` | `None` | Column used by Datashader aggregations that need values. |
| `save` | `True` | Save/emit the Bokeh plot. |
| `display` | `True` | Show the plot. |
| `width`, `height` | `600`, `600` | Plot size for `scatter()`. |
| `source` | `None` | Optional Bokeh `ColumnDataSource`. |
| `tools` | `None` | Optional Bokeh tools string. |
| `size` | `5` / `None` | Marker size. |
| `xlog`, `ylog` | `"auto"` | Log-scale axis control. |
| `outfile` | `None` / `"scatter_grid.html"` | HTML filename, or `"notebook"`. |
| `returnfunc` | `False` | Return Datashader callback instead of attaching it. |
| `span` | `None` | Color-scale span for Datashader output. |
| `cscale` | `"eq_hist"` | Datashader color scaling. |

**Returns**  
Bokeh figure and data source, or a grid/list of figures.

**Example**

```python
fig, source = xplt.scatter(df, "blob_kT", "blob_norm", outfile="notebook")
```

```python
grid = xplt.scatter_grid(
    df[["blob_kT", "blob_norm", "blob_sigma"]],
    sampling=2000,
    outfile="notebook",
)
```

## Spectrum Plotting

### `standard_spectra()`

```python
xmcinter.plots.standard_spectra(
    runpath="../",
    itmin=1,
    itmax=None,
    save=True,
    display=True,
    outfile="spectra.html",
    ylog=False,
    xlog=False,
    logbins=None,
    bins=0.03,
    lastiter=True,
    legacy=False,
    width=1000,
    height=500,
    lines=True,
    **lineargs,
)
```

**Purpose**  
Plot data, average model, and latest model spectra for a run.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `runpath` | `"../"` | XMC run directory. |
| `itmin` | `1` | Minimum spectrum iteration. |
| `itmax` | `None` | Maximum spectrum iteration. |
| `save` | `True` | Save/emit the plot. |
| `display` | `True` | Show the plot. |
| `outfile` | `"spectra.html"` | HTML filename, or `"notebook"`. |
| `ylog`, `xlog` | `False`, `False` | Use log axes. |
| `logbins` | `None` | Use log bins; `None` follows axis settings. |
| `bins` | `0.03` | Spectrum bin size, count, or edges. |
| `lastiter` | `True` | Include latest model spectrum. |
| `legacy` | `False` | Use legacy spectrum filename convention. |
| `width`, `height` | `1000`, `500` | Plot size in pixels. |
| `lines` | `True` | Annotate emission lines. |
| `**lineargs` | none | Extra arguments for line annotation. |

**Example**

```python
fig = xplt.standard_spectra(
    runpath=run,
    itmin=500,
    outfile="notebook",
    ylog=True,
)
```

### `spectra()`

```python
xmcinter.plots.spectra(
    spectra,
    colors=["black", "steelblue", "firebrick"],
    labels=None,
    dashes=None,
    save=True,
    display=True,
    scale=1.0,
    outfile="spectra.html",
    ylog=False,
    xlog=False,
    logbins=None,
    width=1000,
    height=500,
    lines=True,
    **lineargs,
)
```

**Purpose**  
Plot an explicit list of spectrum histogram tuples.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `spectra` | required | List of `(y, yerrors, yedges)` histogram tuples. |
| `colors` | `["black", "steelblue", "firebrick"]` | Plot colors. |
| `labels` | `None` | Legend labels. |
| `dashes` | `None` | Line dash styles. |
| `save` | `True` | Save/emit the plot. |
| `display` | `True` | Show the plot. |
| `scale` | `1.0` | Scale spectrum values. |
| `outfile` | `"spectra.html"` | HTML filename, or `"notebook"`. |
| `ylog`, `xlog` | `False`, `False` | Use log axes. |
| `logbins` | `None` | Use log bins. |
| `width`, `height` | `1000`, `500` | Plot size in pixels. |
| `lines` | `True` | Annotate emission lines. |
| `**lineargs` | none | Extra arguments for line annotation. |

**Example**

```python
fig = xplt.spectra([datahist, avghist], labels=["Data", "Model"], outfile="notebook")
```

### `spectrum_from_blobs()`

```python
xmcinter.plots.spectrum_from_blobs(
    df,
    runpath="../",
    datacolor="black",
    save=True,
    display=True,
    suffix="99999",
    datalabel="Data",
    modelcolor="steelblue",
    modellabel="Model",
    bins=0.03,
    outfile="spectrum_from_blobs.html",
    ylog=False,
    xlog=False,
    logbins=None,
    datarange=None,
    width=1000,
    height=500,
    lines=True,
    **lineargs,
)
```

**Purpose**  
Create and plot a spectrum from a filtered blob subset.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `df` | required | Blob subset DataFrame. |
| `runpath` | `"../"` | XMC run directory. |
| `datacolor` | `"black"` | Data spectrum color. |
| `save` | `True` | Save/emit the plot. |
| `display` | `True` | Show the plot. |
| `suffix` | `"99999"` | Suffix for generated subset files. |
| `datalabel` | `"Data"` | Data legend label. |
| `modelcolor` | `"steelblue"` | Model spectrum color. |
| `modellabel` | `"Model"` | Model legend label. |
| `bins` | `0.03` | Spectrum bin size, count, or edges. |
| `outfile` | `"spectrum_from_blobs.html"` | HTML filename, or `"notebook"`. |
| `ylog`, `xlog` | `False`, `False` | Use log axes. |
| `logbins` | `None` | Use log bins. |
| `datarange` | `None` | Histogram data range. |
| `width`, `height` | `1000`, `500` | Plot size in pixels. |
| `lines` | `True` | Annotate emission lines. |
| `**lineargs` | none | Extra arguments for line annotation. |

**Example**

```python
fig = xplt.spectrum_from_blobs(subset, runpath=run, suffix="99999")
```

## Small Matplotlib Alternative

When Bokeh compatibility gets in the way, use the same DataFrame directly:

```python
import matplotlib.pyplot as plt

plt.scatter(df["blob_kT"], df["blob_norm"], s=5, alpha=0.4)
plt.xlabel("blob_kT")
plt.ylabel("blob_norm")
plt.show()
```
