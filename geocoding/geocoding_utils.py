"""Module contains data to work with positionstack.com API resource."""
import logging
import os
import geocoder
from typing import Tuple, Optional

from dotenv import load_dotenv

from geocoding.geocoding_exceptions import GeneralGeocodingError, UnableToLocateCoordinates

load_dotenv()
COUNTRY_NAME = os.environ.get("COUNTRY_NAME")
GEOCODING_API_KEY = os.environ.get("GEOCODING_API_KEY")

logger = logging.getLogger()


def get_lat_lon_from_city_name(city_name: str) -> Optional[Tuple[str, str]]:
    """Method returns tuple of latitude and longitude in WGS-84 decimal format."""
    # using ArcGis as a geocoding provider
    try:
        response = geocoder.arcgis(city_name)
    except Exception as err:
        logger.error(err)
        raise GeneralGeocodingError("failed to get response from geocoding provider.")
    if not response.ok:
        raise UnableToLocateCoordinates(f"Response status is not 'OK': {response.ok}")
    raw_data = response.geojson.get("features")[0]["properties"]
    latitude = raw_data["lat"]
    longitude = raw_data["lng"]
    return str(latitude), str(longitude)


if __name__ == "__main__":
    print(get_lat_lon_from_city_name(city_name="whsdfadfsgsdfhwe745"))
