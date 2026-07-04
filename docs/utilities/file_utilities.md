# `file_utilities`

`xmcinter.file_utilities` provides small helpers for listing files and reading
simple text file formats. Most users interact with these indirectly through
`xmcinter.xmcfiles`.

```python
import xmcinter.file_utilities as fu
```

## `files_to_list()`

```python
xmcinter.file_utilities.files_to_list(search_dir, search_str="deconvolution.*")
```

**Purpose**  
Return filenames in a directory matching a shell-style pattern.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `search_dir` | required | Directory to inspect. |
| `search_str` | `"deconvolution.*"` | Pattern such as `"deconvolution.*"` or `"statistic.*"`. |

**Returns**  
List of filename strings.

**Example**

```python
files = fu.files_to_list(run, search_str="deconvolution.*")
```

**Notes**

This function returns names from `os.listdir()` filtered with `fnmatch`; sort
the result if order matters.

## `ls_to_list()`

```python
xmcinter.file_utilities.ls_to_list(search_dir, ls_args="")
```

**Purpose**  
Legacy helper that shells out to `ls` and returns output lines as a list.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `search_dir` | required | Directory to inspect. |
| `ls_args` | `""` | Arguments/pattern passed to `ls`. |

**Example**

```python
files = fu.ls_to_list(run, "statistic.*")
```

**Notes**

Prefer `files_to_list()` for new notebook work.

## `parse_file_line()`

```python
xmcinter.file_utilities.parse_file_line(infile, delimiter=",;\\s\\t")
```

**Purpose**  
Parse the first line of a file into tokens. Used by `xmcfiles.read_parnames()`
for `parameters.txt`.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `infile` | required | File path. |
| `delimiter` | `",;\\s\\t"` | Regular-expression delimiter. |

**Returns**  
List of parsed strings.

**Example**

```python
names = fu.parse_file_line(f"{run}/parameters.txt")
```

## `read_list()`

```python
xmcinter.file_utilities.read_list(listfile, comment="")
```

**Purpose**  
Read a text file into a list of non-comment lines.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `listfile` | required | Text file to read. |
| `comment` | `""` | Comment prefix to ignore. |

**Example**

```python
items = fu.read_list("file_list.txt", comment="#")
```

## `file_lines()`

```python
xmcinter.file_utilities.file_lines(infile, comment="")
```

**Purpose**  
Count or return useful lines from a text file while respecting comments.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `infile` | required | Text file to inspect. |
| `comment` | `""` | Comment prefix to ignore. |

**Example**

```python
nlines = fu.file_lines("parameters.txt", comment="#")
```

## `fetch_file()`

```python
xmcinter.file_utilities.fetch_file(search_dir, pat="evt2", prompt=True)
```

**Purpose**  
Find a file matching a pattern in a directory, optionally prompting when there
are zero or multiple matches.

**Parameters**

| Name | Default | Description |
| --- | --- | --- |
| `search_dir` | required | Directory to inspect. |
| `pat` | `"evt2"` | Pattern to search for. |
| `prompt` | `True` | Prompt interactively if no unique match is found. |

**Example**

```python
evtfile = fu.fetch_file("/path/to/obs", pat="evt2", prompt=False)
```

**Notes**

This helper is most useful in older interactive workflows that expected XMM or
Chandra observation products to be nearby.
