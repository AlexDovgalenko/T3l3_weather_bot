"""Module contains data to work with positionstack.com API resource."""
import logging
from typing import Tuple, Optional

import geocoder
from dotenv import load_dotenv

from geocoding.geocoding_exceptions import GeneralGeocodingError, UnableToLocateCoordinates

load_dotenv()

logger = logging.getLogger()


def get_lat_lon_from_city_name(city_name: str) -> Optional[Tuple[str, str]]:
    """Method returns tuple of latitude and longitude in WGS-84 decimal format for provided city name."""
    # using ArcGis as a geocoding provider
    try:
        response = geocoder.arcgis(city_name)
    except Exception as err:
        logger.error(err)
        raise GeneralGeocodingError("failed to get response from geocoding provider.")
    if not response.ok:
        logger.error(response.status)
        raise UnableToLocateCoordinates(f"Response status is not 'OK': {response.status}")
    raw_data = response.geojson.get("features")[0]["properties"]
    latitude = raw_data["lat"]
    longitude = raw_data["lng"]
    logger.info(f"Latitude is: '{latitude}', Longitude is: '{longitude}' for city: {city_name}")
    return str(latitude), str(longitude)


if __name__ == "__main__":
    # print(get_lat_lon_from_city_name(city_name="dispatcher.register_errors_handler(global_error_handler)"))
    print(get_lat_lon_from_city_name(city_name="dispatcher.register_errors_handler(global_error_handler)"))
