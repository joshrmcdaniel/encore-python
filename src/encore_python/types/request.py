import jsonobject


from .shared import valid_per_page, positive_num, valid_hash, instruments, difficulties


class BasicSearch(jsonobject.JsonObject):
    search = jsonobject.StringProperty(name="search")
    per_page = jsonobject.IntegerProperty(
        name="per_page", validators=valid_per_page, required=False, exclude_if_none=True
    )
    page = jsonobject.IntegerProperty(name="page", validators=positive_num, default=1)
    instrument = jsonobject.StringProperty(
        name="instrument", choices=instruments, exclude_if_none=False
    )
    difficulty = jsonobject.StringProperty(
        name="difficulty", choices=difficulties, exclude_if_none=False
    )


class SearchFilter(jsonobject.JsonObject):
    value = jsonobject.StringProperty(name="value", default="")
    exact = jsonobject.BooleanProperty(name="exact", default=False)
    exclude = jsonobject.BooleanProperty(name="exclude", default=False)


class AdvancedSearch(jsonobject.JsonObject):
    instrument = jsonobject.StringProperty(
        name="instrument", choices=instruments, exclude_if_none=False
    )
    page = jsonobject.IntegerProperty(name="page", validators=positive_num, default=1)
    difficulty = jsonobject.StringProperty(
        name="difficulty", choices=difficulties, exclude_if_none=False
    )
    name = jsonobject.ObjectProperty(lambda: SearchFilter, name="name")
    artist = jsonobject.ObjectProperty(lambda: SearchFilter, name="artist")
    album = jsonobject.ObjectProperty(lambda: SearchFilter, name="album")
    genre = jsonobject.ObjectProperty(lambda: SearchFilter, name="genre")
    year = jsonobject.ObjectProperty(lambda: SearchFilter, name="year")
    charter = jsonobject.ObjectProperty(lambda: SearchFilter, name="charter")
    min_length = jsonobject.IntegerProperty(name="minLength", validators=positive_num)
    max_length = jsonobject.IntegerProperty(name="maxLength", validators=positive_num)
    min_intensity = jsonobject.IntegerProperty(
        name="minIntensity", validators=positive_num
    )
    max_intensity = jsonobject.IntegerProperty(
        name="maxIntensity", validators=positive_num
    )
    min_average_nps = jsonobject.IntegerProperty(
        name="minAverageNPS", validators=positive_num
    )
    max_average_nps = jsonobject.IntegerProperty(
        name="maxAverageNPS", validators=positive_num
    )
    min_max_nps = jsonobject.IntegerProperty(name="minMaxNPS", validators=positive_num)
    max_max_nps = jsonobject.IntegerProperty(name="maxMaxNPS", validators=positive_num)
    hash = jsonobject.StringProperty(name="hash", validators=valid_hash)
    chart_hash = jsonobject.StringProperty(name="chartHash", validators=valid_hash)
    modified_after = jsonobject.DateProperty(name="modifiedAfter")
    has_solo_sections = jsonobject.BooleanProperty(name="hasSoloSections")
    has_forced_notes = jsonobject.BooleanProperty(name="hasForcedNotes")
    has_open_notes = jsonobject.BooleanProperty(name="hasOpenNotes")
    has_tap_notes = jsonobject.BooleanProperty(name="hasTapNotes")
    has_lyrics = jsonobject.BooleanProperty(name="hasLyrics")
    has_vocals = jsonobject.BooleanProperty(name="hasVocals")
    has_roll_lanes = jsonobject.BooleanProperty(name="hasRollLanes")
    has_2x_kick = jsonobject.BooleanProperty(name="has2xKick")
    has_issues = jsonobject.BooleanProperty(name="hasIssues")
    has_video_background = jsonobject.BooleanProperty(name="hasVideoBackground")
    modchart = jsonobject.BooleanProperty(name="modchart")
    chart_id_after = jsonobject.IntegerProperty(
        name="chartIdAfter", validators=positive_num, exclude_if_none=True
    )
