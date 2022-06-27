"""Contains custom exceptions described issues with "geocoding_utils.py" module"""


class GeneralGeocodingError(Exception):
    """General error raised from Geocoding module."""


class UnableToLocateCoordinates(GeneralGeocodingError):
    """Error raised when it is failed to get latitude and longitude based on provided city name."""


class GeocodingDataParseError(GeneralGeocodingError):
    """Failed to parse raw geo data from geocoding provider."""
