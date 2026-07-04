# Function Index

This index lists the important public functions documented for notebook
analysis. Lower-level implementation helpers are intentionally omitted unless
they are useful in advanced workflows.

## `xmcinter.xmcfiles`

- [`merge_output()`](../core-modules/xmcfiles.md#merge_output) - merge numbered
  XMC text output files into one DataFrame.
- [`read_parnames()`](../core-modules/xmcfiles.md#read_parnames) - read
  parameter names from `parameters.txt`.
- [`read_spectra()`](../core-modules/xmcfiles.md#read_spectra) - read spectrum
  FITS products into histogram tuples.
- [`fake_deconvolution()`](../core-modules/xmcfiles.md#fake_deconvolution) -
  write a DataFrame back to deconvolution-file format.
- [`remove_nans()`](../core-modules/xmcfiles.md#remove_nans) - drop rows with
  missing values.

## `xmcinter.wrangle`

- [`filterblobs()`](../core-modules/wrangle.md#filterblobs) - filter rows by
  parameter ranges.
- [`simplefilterblobs()`](../core-modules/wrangle.md#simplefilterblobs) -
  single-column filtering helper.
- [`filtercircle()`](../core-modules/wrangle.md#filtercircle) - filter or
  weight blobs by circular regions.
- [`weighted_median()`](../core-modules/wrangle.md#weighted_median) - weighted
  median statistic.
- [`weighted_std()`](../core-modules/wrangle.md#weighted_std) - weighted
  standard deviation.
- [`weighted_modes()`](../core-modules/wrangle.md#weighted_modes) - weighted
  modal estimates.
- [`credible_region()`](../core-modules/wrangle.md#credible_region) - Bayesian
  credible region helper.
- [`make_histogram()`](../core-modules/wrangle.md#make_histogram) - histogram
  helper with optional weights and errors.
- [`normalize_histogram()`](../core-modules/wrangle.md#normalize_histogram) -
  normalize histogram values.
- [`iter_err()`](../core-modules/wrangle.md#iter_err) - estimate per-iteration
  statistic variation.
- [`make_spectrum()`](../core-modules/wrangle.md#make_spectrum) - create a
  spectrum from selected blobs.
- [`normclean()`](../core-modules/wrangle.md#normclean) - advanced
  normalization-based blob cleaning.
- [`line_emissivities()`](../core-modules/wrangle.md#line_emissivities-and-blob_line_photons)
  - line emissivity helper.
- [`blob_line_photons()`](../core-modules/wrangle.md#line_emissivities-and-blob_line_photons)
  - line photon estimate helper.

## `xmcinter.xmcmap`

- [`make_map()`](../core-modules/xmcmap.md#make_map) - create FITS maps and
  return map arrays from blob parameters.
- [`movie_from_stack()`](../core-modules/xmcmap.md#movie_from_stack) - write
  movie frames from an image stack.

## `xmcinter.diagnostics`

- [`check()`](../core-modules/diagnostics.md#check) - run the high-level
  diagnostic workflow.
- [`clean()`](../core-modules/diagnostics.md#clean) - filter iterations and add
  derived blob quantities.

## `xmcinter.plots`

- [`chi2()`](../core-modules/plots.md#chi2) - reduced chi-square convergence
  plot.
- [`trace()`](../core-modules/plots.md#trace) - parameter trace plots.
- [`histogram()`](../core-modules/plots.md#histogram-and-histogram_grid) -
  single weighted/unweighted histogram.
- [`histogram_grid()`](../core-modules/plots.md#histogram-and-histogram_grid) -
  grid of posterior histograms.
- [`scatter()`](../core-modules/plots.md#scatter-and-scatter_grid) - single
  parameter scatter plot.
- [`scatter_grid()`](../core-modules/plots.md#scatter-and-scatter_grid) -
  scatter matrix for blob parameters.
- [`standard_spectra()`](../core-modules/plots.md#standard_spectra) - standard
  data/model spectrum plot.
- [`spectra()`](../core-modules/plots.md#spectra) - plot supplied spectrum
  histogram tuples.
- [`spectrum_from_blobs()`](../core-modules/plots.md#spectrum_from_blobs) -
  create and plot a spectrum from a blob subset.
- `plot_lines()` - add emission-line annotations to an existing Bokeh spectrum
  figure.
- `errorbar()` - add symmetric error bars to a Bokeh figure.

## `xmcinter.astro_utilities`

- [`norm_to_em()`](../utilities/astro_utilities.md#norm_to_em) - convert norm to
  emission measure.
- [`em_to_density()`](../utilities/astro_utilities.md#em_to_density) - estimate
  density from emission measure and volume.
- [`em_to_mass()`](../utilities/astro_utilities.md#em_to_mass-and-em_to_mass2)
  - estimate mass from emission measure and volume.
- [`em_to_mass2()`](../utilities/astro_utilities.md#em_to_mass-and-em_to_mass2)
  - mass estimate using blob size and distance.
- [`convert_distance()`](../utilities/astro_utilities.md#convert_distance) -
  distance unit conversion.
- [`convert_arcsec()`](../utilities/astro_utilities.md#convert_arcsec) -
  angular-to-physical size conversion.
- [`angstroms2keV()`](../utilities/astro_utilities.md#angstroms2kev-and-k2kev)
  - wavelength/energy conversion.
- [`K2keV()`](../utilities/astro_utilities.md#angstroms2kev-and-k2kev) -
  temperature conversion.
- [`gaussian_volume()`](../utilities/astro_utilities.md#gaussian_volume) -
  Gaussian blob volume.
- [`distance()`](../utilities/astro_utilities.md#distance) - 2-D coordinate
  distance.
- [`xmc2wcs()`](../utilities/astro_utilities.md#xmc2wcs-and-wcs2xmc) - convert
  XMC coordinates to sky coordinates.
- [`wcs2xmc()`](../utilities/astro_utilities.md#xmc2wcs-and-wcs2xmc) - convert
  sky coordinates to XMC coordinates.
- [`normalize_image()`](../utilities/astro_utilities.md#normalize_image) -
  normalize a FITS image.
- [`stack_images()`](../utilities/astro_utilities.md#stack_images) - sum aligned
  FITS images.
- [`transfer_header()`](../utilities/astro_utilities.md#transfer_header) - copy
  a FITS header.
- [`xspec_abund_to_nomoto()`](../utilities/astro_utilities.md#xspec_abund_to_nomoto-and-xspec_abund_to_nomoto_dataframe)
  - abundance ratio conversion.
- [`xspec_abund_to_nomoto_dataframe()`](../utilities/astro_utilities.md#xspec_abund_to_nomoto-and-xspec_abund_to_nomoto_dataframe)
  - abundance ratio conversion on DataFrames.
- [`fetch_lines()`](../utilities/astro_utilities.md#fetch_lines-and-show_xray_lines)
  - fetch X-ray line list rows.
- [`show_xray_lines()`](../utilities/astro_utilities.md#fetch_lines-and-show_xray_lines)
  - inspect X-ray line list rows.
- [`redshift_line()`](../utilities/astro_utilities.md#redshift_line-and-distance2redshift)
  - redshift a line energy or wavelength.
- [`distance2redshift()`](../utilities/astro_utilities.md#redshift_line-and-distance2redshift)
  - approximate distance-to-redshift helper.

## `xmcinter.file_utilities`

- [`files_to_list()`](../utilities/file_utilities.md#files_to_list) - list files
  matching a pattern.
- [`ls_to_list()`](../utilities/file_utilities.md#ls_to_list) - legacy
  shell-based file listing.
- [`parse_file_line()`](../utilities/file_utilities.md#parse_file_line) - parse
  a tokenized file line.
- [`read_list()`](../utilities/file_utilities.md#read_list) - read a text list.
- [`file_lines()`](../utilities/file_utilities.md#file_lines) - count/read file
  lines.
- [`fetch_file()`](../utilities/file_utilities.md#fetch_file) - find a file by
  pattern.
