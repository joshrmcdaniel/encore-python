# encore-python
Python API wrapper for encore.us

## Features

- **Music Search**: Perform searches by track name, album, artist, genre, and year with both basic and advanced filtering options.
- **Download Tracks**: Download music tracks directly using the song identifier or a `Song` object.
- **Rate Limit Handling**: Automatically handles API rate limits, providing feedback on the remaining number of queries and reset times.
- **Flexible Search Queries**: Supports both simple string queries and structured search objects (`BasicSearch` and `AdvancedSearch`).

## Installation

To install encore-python, run:

```bash
cd encore-python 
pip install encore-python
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

### Downloading Tracks

To download a track:

```python
# With the hash
song_content = api.download("abcedf....")
# With the song json
search_res = api.search("Query")
song_content = api.download(search_res.data[0])
with open("song_name.sng", "wb") as f:
    f.write(song_content)
```


## Contributing

Contributions to the encore-python are welcome.

## License

encore-python is released under the MIT License. See the LICENSE file in the repository for more details.