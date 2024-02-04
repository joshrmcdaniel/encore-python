from collections.abc import Mapping, Iterable
from typing import Any
from jsonobject import JsonObject, JsonArray

from functools import reduce
from ..types import AdvancedSearch, SearchFilter

DEFAULT_SEARCH = AdvancedSearch()


def _search_filter(search_for: str):
    def inner(
        value: str,
        *adv_filter_objs,
        exact: bool = True,
        exclude: bool = False,
        **filter_kwargs,
    ):
        adv_search = AdvancedSearch()
        if adv_filter_objs:
            adv_search = _concat_filter(*adv_filter_objs)
        if filter_kwargs:
            adv_search.update(**filter_kwargs)
        adv_search[search_for] = SearchFilter(value=value, exact=exact, exclude=exclude)
        return adv_search

    return inner


def _concat_filter(*adv_filters):
    if len(adv_filters) == 1:
        return adv_filters[0]
    return reduce(_update, adv_filters)


def _update(d: Mapping, u: Mapping | str | int | float, *, default_d=None):
    if default_d is None:
        default_d = DEFAULT_SEARCH
    if isinstance(d, (JsonObject, dict)):
        for k, v in u.items():
            k: str
            v: Any
            d[k] = _update(d[k], v, default_d=default_d[k])
    elif isinstance(d, (JsonArray, list)):
        for idx, itm in enumerate(u):
            d[idx] = _update(d[idx], itm[idx], default_d=default_d[idx])
    elif d != u and u != default_d:
        d = u
    return d
