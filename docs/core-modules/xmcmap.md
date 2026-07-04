# `xmcmap`

`xmcinter.xmcmap` turns blob samples into image maps. It is the main tool for
temperature maps, emission maps, abundance maps, and related parameter maps.

```python
import xmcinter.xmcmap as xm
```

## `make_map()`

```python
xmcinter.xmcmap.make_map(
    indata,
    outfile=None,
    paramname="blob_kT",
    paramweights=None,
    binsize=10.0,
    itmod=100,
    paramshape="gauss",
    ctype="median",
    x0=None,
    y0=None,
    imagesize=None,
    witherror=True,
    sigthresh=0.0,
    sigthreshparam=None,
    imgthresh=None,
    imgthreshparam=None,
    paramx="blob_phi",
    paramy="blob_psi",
    paramsize="blob_sigma",
    exclude_region=None,
    iteration_type="median",
    clobber=False,
    nlayers=None,
    parallel=True,
    nproc=3,
    cint=True,
    movie=False,
    moviedir=None,
    cumulativemovie=False,
    withsignificance=False,
    rotation=0.0,
    random_layers=True,
)
```

**Purpose**  
Create a FITS image map from a blob table or from a saved merged deconvolution
file.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `indata` | required | Blob DataFrame or path to a merged deconvolution table. |
| `outfile` | `None` | Output FITS filename prefix. |
| `paramname` | `"blob_kT"` | Column to map, or list of columns. |
| `paramweights` | `None` | Optional weight column or list of weight columns. |
| `binsize` | `10.0` | Pixel size in the same units as `paramx` and `paramy`. |
| `itmod` | `100` | Use every `itmod`-th iteration when `nlayers` is not set. |
| `paramshape` | `"gauss"` | Blob shape: usually `"gauss"`; `"points"` is also supported. |
| `ctype` | `"median"` | Collapse method across iteration images. |
| `x0` | `None` | Map center x-coordinate; `None` estimates from the data. |
| `y0` | `None` | Map center y-coordinate; `None` estimates from the data. |
| `imagesize` | `None` | Output image size; `None` estimates from the data. |
| `witherror` | `True` | Append an error map extension to the FITS file. |
| `sigthresh` | `0.0` | Significance threshold below which pixels are set to NaN. |
| `sigthreshparam` | `None` | Parameter map used for significance thresholding. |
| `imgthresh` | `None` | Pixel-value threshold below which pixels are set to NaN. |
| `imgthreshparam` | `None` | Parameter map used for image thresholding. |
| `paramx` | `"blob_phi"` | X-coordinate column. |
| `paramy` | `"blob_psi"` | Y-coordinate column. |
| `paramsize` | `"blob_sigma"` | Blob size column. |
| `exclude_region` | `None` | Optional circular region `(x0, y0, radius)` to mask. |
| `iteration_type` | `"median"` | Combine method within each iteration image. Use `"total"` for emission-like quantities. |
| `clobber` | `False` | Overwrite existing FITS files. |
| `nlayers` | `None` | Number of iteration layers to use; overrides `itmod`. |
| `parallel` | `True` | Use multiprocessing for iteration images. |
| `nproc` | `3` | Number of worker processes when `parallel=True`. |
| `cint` | `True` | Use compiled `gaussian.so` for Gaussian integration. Use `False` for portability. |
| `movie` | `False` | Save individual layer images for a movie. |
| `moviedir` | `None` | Output directory for movie frames. |
| `cumulativemovie` | `False` | Make movie frames cumulative across layers. |
| `withsignificance` | `False` | Append a significance map extension. |
| `rotation` | `0.0` | Rotate final images by this many degrees. |
| `random_layers` | `True` | Select random layers when `nlayers` is set. |

**Returns**  
List of NumPy image arrays. The function also writes FITS files.

**Typical workflow**

```python
imgs = xm.make_map(
    df,
    paramname="blob_kT",
    paramweights="blob_norm",
    binsize=30.0,
    iteration_type="median",
    ctype="median",
    outfile="temperature",
    clobber=True,
    cint=False,
)
```

**Notes**

- Use `iteration_type="total"` for summed quantities such as `blob_norm` or
  `blob_em`.
- Use weights for physical parameter maps when appropriate. A common temperature
  map uses `paramname="blob_kT"` and `paramweights="blob_norm"` or
  `paramweights="blob_em"`.
- `make_map()` currently writes FITS output before returning arrays; there is no
  public `save=False` mode.
- The `sphere` blob-shape implementation is marked as not functional in the
  source comments. Gaussian blobs are the normal path.

**Emission map example**

```python
em_imgs = xm.make_map(
    df,
    paramname="blob_norm",
    paramweights=None,
    binsize=30.0,
    iteration_type="total",
    ctype="median",
    outfile="emission",
    clobber=True,
    cint=False,
)
```

**Display returned array**

```python
import matplotlib.pyplot as plt

plt.imshow(imgs[0], origin="lower", cmap="plasma")
plt.colorbar(label="blob_kT")
plt.show()
```

## `movie_from_stack()`

```python
xmcinter.xmcmap.movie_from_stack(
    stack,
    moviedir,
    cumulativemovie=False,
    ctype="median",
    delay=20,
    cmap="CMRmap",
    parallel=True,
)
```

**Purpose**  
Write image frames from a stack of iteration images so that an external tool can
assemble a movie.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `stack` | required | 3-D image stack. |
| `moviedir` | required | Output directory for frames. |
| `cumulativemovie` | `False` | Use cumulative images instead of individual layers. |
| `ctype` | `"median"` | Collapse mode when cumulative. |
| `delay` | `20` | Frame delay metadata. |
| `cmap` | `"CMRmap"` | Matplotlib colormap name. |
| `parallel` | `True` | Use multiprocessing where supported. |

**Returns**  
Writes image files; intended for visualization workflows.

**Example**

```python
xm.movie_from_stack(stack, moviedir="temperature_movie", cmap="inferno")
```

## Lower-Level Mapping Functions

The module also contains lower-level functions such as `iteration_image()`,
`collapse_stack()`, and Gaussian integration helpers. These are useful for
understanding or debugging `make_map()`, but typical analysis notebooks should
call `make_map()` directly.
