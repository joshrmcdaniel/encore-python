from dataclasses import dataclass
from datetime import datetime as dt
from typing import Any, Dict


import requests

from .parsing import _search_filter
from ..types import BasicSearch, AdvancedSearch, SearchFilter, SearchResponse, ErrorResponse

@dataclass
class EncoreAPI:
    _ratelimit_left = 0
    _ratelimit_reset = dt.fromtimestamp(0)
    _ratelimit_total = 50
    SEARCH_URL = "https://api.enchor.us"
    DOWNLOAD_URL = "https://files.enchor.us"

    create_name_filter = staticmethod(_search_filter('name'))
    create_album_filter = staticmethod(_search_filter('album'))
    create_genre_filter = staticmethod(_search_filter('genre'))
    create_year_filter = staticmethod(_search_filter('year'))
    create_artist_filter = staticmethod(_search_filter('artist'))
    create_charter_filter = staticmethod(_search_filter('charter'))


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

    def _search(self, *, query_json: Dict[str, Any], advanced: bool):
        endpoint = "/search"
        if advanced:
            endpoint += "/advanced"
        return requests.post(self.SEARCH_URL+ endpoint, json=query_json)
    
    def _set_rate_limit_info(self, r: requests.Response):
        self.ratelimit_total = r.headers["X-RateLimit-Limit"]
        self.ratelimit_reset = r.headers["X-RateLimit-Reset"]
        self.ratelimit_left = r.headers["X-RateLimit-Remaining"]

    def search_by_artist(
        self,
        artist: str,
        *,
        exact: bool = True,
        exclude: bool = False,
        **additional_filters
    ):
        adv_search = AdvancedSearch(
            artist=SearchFilter(
                value=artist,
                exact=exact,
                exclude=exclude
            ),
            **additional_filters
        )

        return self.search(adv_search)

    def search_by_album(
        self,
        album: str,
        *,
        artist: str = None,
        exact: bool = True,
        exclude: bool = False,
        **additional_filters
    ) -> SearchResponse | ErrorResponse:
        album_params = SearchFilter(value=album, exact=exact, exclude=exclude)
        adv_search = AdvancedSearch(album=album_params, **additional_filters)
        if artist:
            adv_search.artist = SearchFilter(value=artist, exact=exact, exclude=exclude)

        return self.search(adv_search)
    

    @property
    def ratelimit_reset(self):
        return self._ratelimit_reset
    
    @ratelimit_reset.setter
    def ratelimit_reset(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_reset = dt.fromtimestamp(value)
    
    @property
    def ratelimit_left(self):
        return self._ratelimit_left
    
    @ratelimit_left.setter
    def ratelimit_left(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_left = value
    
    @property
    def ratelimit_total(self):
        return self._ratelimit_total
    
    @ratelimit_total.setter
    def ratelimit_total(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_total = value



    @property
    def headers(self):
        return {
            "Accept": "application/json"
        }