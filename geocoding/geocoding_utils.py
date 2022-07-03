"""Module contains data to work with positionstack.com API resource."""

from dataclasses import dataclass
from typing import Tuple, Optional, List

import geocoder
from loguru import logger

from geocoding.geocoding_exceptions import GeneralGeocodingError, UnableToLocateCoordinates, GeocodingDataParseError


@dataclass
class LocationPoint:
    lat_lon: str
    address: str


def get_available_location_options(city_name: str) -> List[LocationPoint]:
    """Returns list of available options from geocoding provider by supplied city name"""
    try:
        raw_response = geocoder.arcgis(location=city_name, maxRows=10)
    except Exception as err:
        logger.error(err)
        raise GeneralGeocodingError("Failed to get response from geocoding provider.")
    if not raw_response.ok:
        logger.error(raw_response.status)
        raise UnableToLocateCoordinates(f"Response status is not 'OK': {raw_response.status}")
    filtered_result = __filter_geo_locations(raw_response)
    if not filtered_result:
        err_msg = f"Response status is 'OK': but filtered list of available locations for city name '{city_name}' " \
                  f"is empty."
        logger.error(err_msg)
        raise UnableToLocateCoordinates(err_msg)
    no_duplicates_list = __filter_location_duplicates(filtered_result)
    return __parse_raw_geo_output(no_duplicates_list)


def get_lat_lon_from_attribute(lat_lon: str) -> Optional[Tuple[str, str]]:
    """Returns tuple of latitude and longitude in WGS-84 decimal format for provided lat-lon argument"""
    # Using ArcGis as a geocoding provider
    # Maximum number of available locations limited to 10 for more convenience

    raw_data = lat_lon.split("-")
    latitude = raw_data[0]
    longitude = raw_data[1]
    logger.info(f"Latitude is: '{latitude}', Longitude is: '{longitude}'")
    return latitude, longitude


def __filter_geo_locations(geo_list) -> List[dict]:
    """Function filters out only those options which have Addr_type=Locality
    For more information refer to the official ArcGis documentation

    :param geo_list:
    :return: list of available locations
    """
    if not geo_list.geojson:
        raise UnableToLocateCoordinates(f"Response 'geojson' object is empty")
    return list(
        filter(lambda location: location["properties"]["quality"] == "Locality", geo_list.geojson.get("features")))


def __drop_locations_duplicates(locations_list):
    """Drops location duplicates if lat_lon in the list equals."""
    pass


def __parse_raw_geo_output(raw_geo_list) -> List[LocationPoint]:
    """Method parses raw list of geo-locations items into list of LocationPoint elements"""
    location_points_list = []
    try:
        for item in raw_geo_list:
            location_points_list.append(
                LocationPoint(lat_lon=f"{item['properties']['lat']}-{item['properties']['lng']}",
                              address=item['properties']["address"]))
    except Exception as exception:
        err_msg = f"Failed to parse raw geolocation data to 'LocationPoint' structure\n{exception}"
        logger.error(err_msg)
        raise GeocodingDataParseError(err_msg)
    return location_points_list


def __get_locations_geometry(geo_list: List[dict]) -> List[list]:
    """Method to filters out list of available geolocations"""
    if not geo_list:
        return []
    return [item["geometry"] for item in geo_list]


def __filter_location_duplicates(geo_list: List[dict]) -> List[dict]:
    """Filter out location duplicates by same geo coordinates.

    :param geo_list: raw list of available geolocations
    :return: filtered list of geolocations without duplicates
    """
    result_list = []
    for location in range(len(geo_list)):
        if geo_list[location].get("geometry") not in __get_locations_geometry(result_list):
            result_list.append(geo_list[location])
    return result_list


if __name__ == "__main__":
    # result = geocoder.arcgis(location='Черноморское', maxRows=10)
    result = get_available_location_options(city_name='Черноморское')
    print(result)
