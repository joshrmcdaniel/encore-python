from dataclasses import dataclass
from datetime import datetime as dt
from typing import Any, Callable, Optional, Tuple, Mapping, Final


import requests

from .parsing import _search_filter
from ..types import (
    BasicSearch,
    BasicSearchOpts,
    AdvancedSearch,
    AdvancedSearchOpts,
    SearchResponse,
    ErrorResponse,
)

from ..types.request import EncoreRequestHeaders

__all__ = [
    "EncoreAPI"
]

@dataclass
class EncoreAPI:
    """
    Provides a Python interface to interact with the Encore music search and download API.

    This class encapsulates methods for searching music tracks based on various filters,
    handling rate limits, and constructing search filter objects dynamically.

    Attributes:
        _ratelimit_left (int): Tracks the remaining number of requests that can be made before rate limiting.
        _ratelimit_reset (datetime): The time when the rate limit counter will reset.
        _ratelimit_total (int): The total number of requests allowed within the rate limit window.
        SEARCH_URL (str): Base URL for the search API endpoint.
        DOWNLOAD_URL (str): Base URL for the download API endpoint.

    Methods:
        search: Performs a search operation using either a string query, a `BasicSearch`, or an `AdvancedSearch` object.
        search_by_artist: Convenience method for searching by artist name with optional additional filters.
        search_by_album: Convenience method for searching by album name with optional additional filters and artist name.
        _search: Internal method to execute the search request against the Encore API.
        _set_rate_limit_info: Internal method to update rate limit information from the API response headers.

    Properties:
        ratelimit_reset: Getter and setter for the rate limit reset time.
        ratelimit_left: Getter and setter for the remaining rate limit count.
        ratelimit_total: Getter and setter for the total rate limit count.
        headers: Returns the default headers used for API requests, mainly for accepting JSON responses.
    """

    _ratelimit_left: int = 0
    _ratelimit_reset: dt = dt.fromtimestamp(0)
    _ratelimit_total: int = 50
    SEARCH_URL: Final = "https://api.enchor.us"
    DOWNLOAD_URL: Final = "https://files.enchor.us"

    create_name_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("name"))
    create_album_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("album"))
    create_genre_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("genre"))
    create_year_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("year"))
    create_artist_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("artist"))
    create_charter_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("charter"))

    def search(
        self,
        query: str | AdvancedSearch | BasicSearch,
        *,
        per_page: int = 20,
        page: int = 1,
        instrument: str = None,
        difficulty: str = None,
    ) -> SearchResponse | ErrorResponse:
        if isinstance(query, str):
            query = BasicSearch(
                search=query,
                per_page=per_page,
                page=page,
                instrument=instrument,
                difficulty=difficulty,
            )
        adv_search = isinstance(query, AdvancedSearch)
        # Assuming query is a search object
        query = query.to_json()
        if self.ratelimit_left == 0 and (x := dt.now()) < self.ratelimit_reset:
            print(f"Cannot search, wait until {x.isoformat()}")
            return
        res = self._search(query_json=query, advanced=adv_search)
        self._set_rate_limit_info(res)
        try:
            res.raise_for_status()
            return SearchResponse(res.json())
        except:
            return ErrorResponse(res.json())

    def _search(self, *, query_json: BasicSearchOpts | AdvancedSearchOpts, advanced: bool) -> requests.Response:
        endpoint = "/search"
        if advanced:
            endpoint += "/advanced"
        return requests.post(self.SEARCH_URL + endpoint, json=query_json)

    def _set_rate_limit_info(self, r: requests.Response):
        self.ratelimit_total = r.headers["X-RateLimit-Limit"]
        self.ratelimit_reset = r.headers["X-RateLimit-Reset"]
        self.ratelimit_left = r.headers["X-RateLimit-Remaining"]

    def search_by_artist(
        self,
        artist: str,
        *adv_filter_objs: Tuple[AdvancedSearch],
        exact: bool = True,
        exclude: bool = False,
        **additional_filters: AdvancedSearchOpts,
    ) -> SearchResponse | ErrorResponse:
        adv_search = self.create_artist_filter(
            artist, *adv_filter_objs, exact=exact, exclude=exclude, **additional_filters
        )

        return self.search(adv_search)

    def search_by_album(
        self,
        album: str,
        *adv_filter_objs: Tuple[AdvancedSearch],
        artist: Optional[str] = None,
        exact: bool = True,
        exclude: bool = False,
        **additional_filters: AdvancedSearchOpts,
    ) -> SearchResponse | ErrorResponse:
        params = self.create_album_filter(
            album, *adv_filter_objs, exact=exact, exclude=exclude, **additional_filters
        )
        if artist:
            params = self.create_artist_filter(
                artist, params, exact=exact, exclude=exclude
            )

        return self.search(params)

    @property
    def ratelimit_reset(self) -> dt:
        return self._ratelimit_reset

    @ratelimit_reset.setter
    def ratelimit_reset(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_reset = dt.fromtimestamp(value)

    @property
    def ratelimit_left(self) -> int:
        return self._ratelimit_left

    @ratelimit_left.setter
    def ratelimit_left(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_left = value

    @property
    def ratelimit_total(self) -> int:
        return self._ratelimit_total

    @ratelimit_total.setter
    def ratelimit_total(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_total = value

    @property
    def headers(self) -> EncoreRequestHeaders:
        return {"Accept": "application/json"}
