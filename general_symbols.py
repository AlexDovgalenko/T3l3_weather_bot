from enum import Enum


class GeneralEmojis(Enum):
    """Represents general Emojis set used in bot app."""
    EXCLAMATION_MARK_RED = "\U00002757"
    CHECK_MARK = "\U00002705"
    GLOWING_STAR = "\U0001F31F"
    HOUSE = "\U0001F3E1"
    WARNING = "\U000026A0"
    OPTIONS = "\U0001F6E0"
    WEATHER_FORECAST = "\U0001F324"
    EMPTY_CELL_EMOJI = "\U00002065"
    POOP = "\U0001F4A9"
    CROSSED_FLAGS = "\U0001F38C"
    UA_FLAG = "\U0001F1FA\U0001F1E6"
    US_FLAG = "\U0001F1FA\U0001F1F8"


class SpecialSymbols(Enum):
    """Represents general Special symbols set used in bot app."""
    BULLET_MARK = "➣"
    BULLET_ARROW_1 = "➪"
    BULLET_ARROW_2 = "➫"
    ARROW_UP = "⇪"
    TRIANGLE_LEFT = "◄"
    TRIANGLE_RIGHT = "►"
    TRIANGLE_UP = "▲"
    TRIANGLE_DOWN = "▼"
    CELCIUM_DEGREE = "℃"
    EMPTY_CHAR = "\U00002800"
