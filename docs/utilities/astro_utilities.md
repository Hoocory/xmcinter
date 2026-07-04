# `astro_utilities`

`xmcinter.astro_utilities` contains unit conversions, emission-measure helpers,
abundance conversions, FITS image utilities, and line-list utilities used by the
analysis workflow.

```python
import xmcinter.astro_utilities as astro
```

## Emission Measure, Density, and Mass

### `norm_to_em()`

```python
xmcinter.astro_utilities.norm_to_em(norm, dist_cm, redshift=0.0)
```

**Purpose**  
Convert an XSPEC/XMC normalization to emission measure.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `norm` | required | Model normalization. |
| `dist_cm` | required | Distance in cm. |
| `redshift` | `0.0` | Optional redshift correction. |

**Returns**  
Emission measure.

**Example**

```python
dist_cm = astro.convert_distance(3.3, "kpc", "cm")
df["blob_em"] = astro.norm_to_em(df["blob_norm"], dist_cm)
```

### `em_to_density()`

```python
xmcinter.astro_utilities.em_to_density(
    em,
    volume,
    density_type="number",
    mu=1.21,
)
```

**Purpose**  
Estimate gas density from emission measure and volume.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `em` | required | Emission measure. |
| `volume` | required | Emitting volume. |
| `density_type` | `"number"` | Density type to return. |
| `mu` | `1.21` | Mean molecular weight factor. |

**Example**

```python
df["blob_numberdensity"] = astro.em_to_density(
    df["blob_em"],
    df["blob_volume"],
    density_type="number",
)
```

### `em_to_mass()` and `em_to_mass2()`

```python
xmcinter.astro_utilities.em_to_mass(em, volume, mu=1.21, tounit="g")
xmcinter.astro_utilities.em_to_mass2(
    em,
    sigma,
    beta=1.21,
    tounit="g",
    distance=50.0,
    distanceunit="kpc",
    mu=1.0,
)
```

**Purpose**  
Estimate mass from emission measure. `em_to_mass2()` is used by the diagnostic
cleaning workflow with blob size and distance.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `em` | required | Emission measure. |
| `volume` | required for `em_to_mass()` | Emitting volume. |
| `sigma` | required for `em_to_mass2()` | Blob Gaussian size. |
| `mu` | `1.21` / `1.0` | Mean molecular weight factor. |
| `beta` | `1.21` | Composition factor used by `em_to_mass2()`. |
| `tounit` | `"g"` | Output mass unit. |
| `distance` | `50.0` | Distance for `em_to_mass2()`. |
| `distanceunit` | `"kpc"` | Unit of `distance`. |

**Example**

```python
df["blob_mass"] = astro.em_to_mass(df["blob_em"], df["blob_volume"], tounit="sol")
```

## Unit Conversion

### `convert_distance()`

```python
xmcinter.astro_utilities.convert_distance(val, fromunit, tounit)
```

**Purpose**  
Convert distances among supported units.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `val` | required | Distance value. |
| `fromunit` | required | Input unit. |
| `tounit` | required | Output unit. |

**Example**

```python
dist_cm = astro.convert_distance(3.3, "kpc", "cm")
```

### `convert_arcsec()`

```python
xmcinter.astro_utilities.convert_arcsec(theta, distance, distanceunit, tounit)
```

**Purpose**  
Convert angular sizes to physical sizes using a distance.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `theta` | required | Angular size in arcseconds. |
| `distance` | required | Source distance. |
| `distanceunit` | required | Unit of `distance`. |
| `tounit` | required | Desired physical output unit. |

**Example**

```python
sigma_cm = astro.convert_arcsec(df["blob_sigma"], 3.3, "kpc", "cm")
```

### `angstroms2keV()` and `K2keV()`

```python
xmcinter.astro_utilities.angstroms2keV(inwave)
xmcinter.astro_utilities.K2keV(temperature, reverse=False)
```

**Purpose**  
Convert wavelengths to energies and temperatures to keV.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `inwave` | required | Wavelength in Angstroms. |
| `temperature` | required | Temperature value. |
| `reverse` | `False` | Convert keV to K when `True`. |

**Example**

```python
energy = astro.angstroms2keV(12.4)
kT = astro.K2keV(1.0e7)
```

## Geometry and Coordinates

### `gaussian_volume()`

```python
xmcinter.astro_utilities.gaussian_volume(sigma)
```

**Purpose**  
Calculate the volume of a spherical Gaussian blob from `sigma`.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `sigma` | required | Gaussian sigma in the desired length unit. |

**Example**

```python
df["blob_volume"] = astro.gaussian_volume(sigma_cm)
```

### `distance()`

```python
xmcinter.astro_utilities.distance(x, y, x0=-60.0, y0=80.0)
```

**Purpose**  
Compute distance in a 2-D coordinate plane.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `x` | required | X coordinate(s). |
| `y` | required | Y coordinate(s). |
| `x0` | `-60.0` | Reference x coordinate. |
| `y0` | `80.0` | Reference y coordinate. |

**Example**

```python
df["radius"] = astro.distance(df["blob_phi"], df["blob_psi"], x0=0.0, y0=0.0)
```

### `xmc2wcs()` and `wcs2xmc()`

```python
xmcinter.astro_utilities.xmc2wcs(phi, psi, attfile="atthk.fits")
xmcinter.astro_utilities.wcs2xmc(ra, dec, attfile="atthk.fits")
```

**Purpose**  
Convert between XMC coordinates and sky coordinates using an attitude file.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `phi`, `psi` | required | XMC coordinates. |
| `ra`, `dec` | required | Sky coordinates. |
| `attfile` | `"atthk.fits"` | Attitude file used for the coordinate transform. |

**Example**

```python
ra, dec = astro.xmc2wcs(df["blob_phi"], df["blob_psi"], attfile="atthk.fits")
```

These functions require appropriate observation attitude files.

## FITS Image Utilities

### `normalize_image()`

```python
xmcinter.astro_utilities.normalize_image(infile, outfile="default")
```

**Purpose**  
Normalize a FITS image so that its pixels sum to one.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `infile` | required | Input FITS image. |
| `outfile` | `"default"` | Output filename. `"default"` appends `.norm`. |

**Returns**  
Normalized image array and writes an output FITS file.

**Example**

```python
img = astro.normalize_image("emission_total_blob_norm.fits")
```

### `stack_images()`

```python
xmcinter.astro_utilities.stack_images(infiles, outfile="default")
```

**Purpose**  
Sum aligned FITS images into a stacked image.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `infiles` | required | List of FITS image filenames. |
| `outfile` | `"default"` | Output FITS filename. |

**Example**

```python
stack = astro.stack_images(["map1.fits", "map2.fits"], outfile="stacked.fits")
```

### `transfer_header()`

```python
xmcinter.astro_utilities.transfer_header(sourcefile, targetfile, newfile)
```

**Purpose**  
Copy a FITS header from one file to another.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `sourcefile` | required | FITS file that provides the header. |
| `targetfile` | required | FITS file that provides the image/data. |
| `newfile` | required | Output FITS file. |

**Example**

```python
astro.transfer_header("reference.fits", "map.fits", "map_with_header.fits")
```

## Abundances and Line Lists

### `xspec_abund_to_nomoto()` and `xspec_abund_to_nomoto_dataframe()`

```python
xmcinter.astro_utilities.xspec_abund_to_nomoto(
    specZ,
    refZ,
    specZerr=0.0,
    refZerr=0.0,
)
xmcinter.astro_utilities.xspec_abund_to_nomoto_dataframe(
    df,
    specZcol,
    refZcol,
    specZerrcol=None,
    refZerrcol=None,
)
```

**Purpose**  
Convert XSPEC abundances to Nomoto-style abundance ratios.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `specZ`, `refZ` | required | Abundance values for the species and reference element. |
| `specZerr`, `refZerr` | `0.0` | Optional abundance uncertainties. |
| `df` | required for DataFrame wrapper | Input DataFrame. |
| `specZcol`, `refZcol` | required for DataFrame wrapper | Species/reference abundance columns. |
| `specZerrcol`, `refZerrcol` | `None` | Optional uncertainty columns. |

**Example**

```python
df["blob_SFe"] = astro.xspec_abund_to_nomoto_dataframe(df, "blob_S", "blob_Fe")
```

### `fetch_lines()` and `show_xray_lines()`

```python
xmcinter.astro_utilities.fetch_lines(
    redshift=0.0,
    kT_range=(0.1, 10.0),
    emissivity_range=(1e-18, 1.0),
    energy_range=None,
    wavelength_range=None,
    nlines=None,
    include_lines=None,
    atomdb=None,
    total=False,
)
xmcinter.astro_utilities.show_xray_lines(**fetchargs)
```

**Purpose**  
Fetch and inspect X-ray emission lines from the package line list.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `redshift` | `0.0` | Redshift applied to line positions. |
| `kT_range` | `(0.1, 10.0)` | Temperature range to include. |
| `emissivity_range` | `(1e-18, 1.0)` | Emissivity range to include. |
| `energy_range` | `None` | Optional energy range. |
| `wavelength_range` | `None` | Optional wavelength range. |
| `nlines` | `None` | Maximum number of lines. |
| `include_lines` | `None` | Optional list of line/element labels to include. |
| `atomdb` | `None` | Optional line-list table. |
| `total` | `False` | Return total emissivity-style output where supported. |
| `**fetchargs` | none | Arguments passed from `show_xray_lines()` to `fetch_lines()`. |

**Example**

```python
lines = astro.fetch_lines(kT_range=(0.5, 2.0), energy_range=(0.8, 2.0))
```

### `redshift_line()` and `distance2redshift()`

```python
xmcinter.astro_utilities.redshift_line(line, z, fromunit="angstroms")
xmcinter.astro_utilities.distance2redshift(d, fromunit="kpc")
```

**Purpose**  
Apply redshift corrections to line energies or wavelengths.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `line` | required | Line wavelength or energy. |
| `z` | required | Redshift. |
| `fromunit` | `"angstroms"` / `"kpc"` | Input unit for the conversion. |
| `d` | required for `distance2redshift()` | Distance value. |

**Example**

```python
observed = astro.redshift_line(1.85, z=0.01, fromunit="keV")
```
