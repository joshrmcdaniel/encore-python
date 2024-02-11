# encore-python
Python API wrapper for encore.us

## Features

- **Music Search**: Perform searches by track name, album, artist, genre, and year with both basic and advanced filtering options.
- **Download Tracks**: Download music tracks directly using the song identifier or a `Song` object.
- **Rate Limit Handling**: Automatically handles API rate limits, providing feedback on the remaining number of queries and reset times.
- **Flexible Search Queries**: Supports both simple string queries and structured search objects (`BasicSearch` and `AdvancedSearch`).

## Instalation
###  From pip
``` shell
pip install encore-python
```

###  From repository
``` shell
git clone https://github.com/joshrmcdaniel/encore-python.git
cd encore-python
pip install -e .
```

## Usage

### Basic Search

To perform a basic search by track name, album, artist, genre, or year:

```python
from encore_python import EncoreAPI

api = EncoreAPI()

# Basic search by track name
response = api.search("Track Name")
```

### Advanced Search

For more complex queries involving multiple criteria:

```python
# Advanced search by artist with additional filters
response = api.search_by_artist("Artist Name", exact=True)
```
### Iterating search results
The ability to iterate through all results is avaiable with the `iter_results` arg

### Downloading Tracks
Downloading tracks is available. Available options include: sng file, convert from the sng format to the directory format, and returning a buffer. 


To download a track:

```python
# With the hash as a sng file
api.download("abcedf....")
# With the song json
search_res = api.search("Jeff")
song = search_res.data[0]
api.download(song)
```
This will download a track into the current working directory with the filename of the download hash, with `.sng`

Downloading a track and converting it

``` python
search_res = api.search("Jeff")
song = search_res.data[0]
api.download(song, as_sng=False)
```

See [sng-format-python](https://github.com/joshrmcdaniel/sng-format-python/blob/v1.1.0/README.md#usage) docs for other sng conversion args.

## Contributing

Contributions to the encore-python are welcome.

## License

encore-python is released under the MIT License. See the LICENSE file in the repository for more details.

