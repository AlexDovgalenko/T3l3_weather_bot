from enum import Enum
from pprint import pprint
from typing import Optional, Tuple

from weather_providers.weather_provider_strategy import WeatherProviderName

WEATHER_EMOJI = {
    "CLEAR_SKY": ("\U00002600", "Ясно", "Clear"),
    "CLOUDS": ("\U00002601", "Хмарно", "Cloudy"),
    "CLOUD_WITH_RAIN": ("\U0001F328", "Дощі", "Rainy"),
    "SNOWFLAKE": ("\U00002744", "Сніг", "Snowy"),
    "SUN_BEHIND_CLOUD": ("\U0001F324", "Хмарно з проясненнями", "Sun and Clouds"),
    "THUNDERSTORM": ("\U000026C8", "Гроза", "Thunderstorm"),
    "DRIZZLE": ("\U000026C6", "Морось", "Drizzle"),
    "FOG_DUST": ("\U0001F32B", "Туман / Попіл", "Gog / Dust")
}


class OpenweathermapWeatherConditionsCodeRanges(Enum):
    CLEAR_SKY = (800,),
    CLOUDS = (803, 804),
    CLOUD_WITH_RAIN = (500, 501, 502, 503, 504, 511, 520, 521, 522, 531),
    SNOWFLAKE = (600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622),
    SUN_BEHIND_CLOUD = (801, 802),
    THUNDERSTORM = (200, 201, 202, 210, 211, 212, 221, 230, 231, 232),
    DRIZZLE = (300, 301, 302, 310, 311, 312, 313, 314, 321),
    FOG_DUST = (701, 711, 721, 731, 741, 751, 761, 762, 771, 781),


class MetromaticsWeatherConditionsCodeRanges(Enum):
    CLEAR_SKY = (1, 101),
    CLOUDS = (3, 4, 103, 104),
    CLOUD_WITH_RAIN = (5, 6, 8, 10, 105, 106, 108, 110),
    SNOWFLAKE = (7, 9, 13, 107, 109, 113),
    SUN_BEHIND_CLOUD = (2, 102),
    THUNDERSTORM = (14, 114),
    DRIZZLE = (15, 115),
    FOG_DUST = (11, 12, 16, 111, 112, 116),


def get_weather_emojy(weather_provider_name: "str", weather_code: int) -> Optional[Tuple[str]]:
    if weather_provider_name == WeatherProviderName.OPENWEATHERMAP.value:
        emoji_class = OpenweathermapWeatherConditionsCodeRanges
    elif weather_provider_name == WeatherProviderName.METEOMATICS.value:
        emoji_class = MetromaticsWeatherConditionsCodeRanges
    else:
        return None
    for item in list(emoji_class):
        if weather_code in item.value[0]:
            weather_descr = item.name
        else:
            continue
        return WEATHER_EMOJI.get(weather_descr)


if __name__ == "__main__":
    pprint(get_weather_emojy("openweathermap", 615))
