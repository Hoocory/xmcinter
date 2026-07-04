# Tutorial: Creating Maps

This tutorial starts from a filtered DataFrame such as `df_conv` from
[Filtering Blobs](filtering-blobs.md).

```python
import numpy as np
import matplotlib.pyplot as plt
import xmcinter.xmcmap as xm
```

Make sure Gaussian blob size is available:

```python
if "blob_sigma" not in df_conv.columns and "blob_lnsigma" in df_conv.columns:
    df_conv["blob_sigma"] = np.exp(df_conv["blob_lnsigma"])
```

## Temperature Map

Use a weighted median-like map for physical parameters such as temperature:

```python
temp_imgs = xm.make_map(
    df_conv,
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

Display the returned array:

```python
plt.imshow(temp_imgs[0], origin="lower", cmap="plasma")
plt.colorbar(label="blob_kT")
plt.title("Temperature map")
plt.show()
```

## Emission / Norm Map

For summed quantities, use `iteration_type="total"`.

```python
norm_imgs = xm.make_map(
    df_conv,
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

```python
plt.imshow(norm_imgs[0], origin="lower", cmap="inferno")
plt.colorbar(label="blob_norm")
plt.title("Emission proxy")
plt.show()
```

## Physical Emission Measure Map

If your DataFrame has `blob_em`, map it directly:

```python
em_imgs = xm.make_map(
    df_conv,
    paramname="blob_em",
    paramweights=None,
    binsize=30.0,
    iteration_type="total",
    ctype="median",
    outfile="emission_measure",
    clobber=True,
    cint=False,
)
```

## Multiple Maps on the Same Grid

```python
imgs = xm.make_map(
    df_conv,
    paramname=["blob_norm", "blob_kT"],
    paramweights=[None, "blob_norm"],
    iteration_type=["total", "median"],
    binsize=30.0,
    outfile="combined",
    clobber=True,
    cint=False,
)
```

## Error and Significance Extensions

```python
imgs = xm.make_map(
    df_conv,
    paramname="blob_norm",
    paramweights=None,
    iteration_type="total",
    witherror=True,
    withsignificance=True,
    outfile="norm_with_errors",
    clobber=True,
    cint=False,
)
```

The primary image is written to FITS HDU 0. Error and significance maps are
appended as additional HDUs when requested.

## Reading a Saved FITS Map

```python
from astropy.io import fits

img = fits.getdata("temperature_median_blob_kT.fits", 0)

plt.imshow(img, origin="lower", cmap="plasma")
plt.colorbar()
plt.show()
```

## Choosing `cint`

Use `cint=False` while learning or when `gaussian.so` is not built for your
machine. Use `cint=True` only after rebuilding `gaussian.so` locally.
