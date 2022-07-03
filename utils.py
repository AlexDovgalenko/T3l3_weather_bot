"""Module contains useful tools"""

from loguru import logger


def math_round(digit):
    """Performs mathematical rounding e.g. 0.4 -> 0, 1.5 -> 2
    input  [0.4, 0.5, 0.1, 1.2, 1.4, 1.5, 9.19, 13.1]
    output [0, 1, 0, 1, 1, 2, 10, 13]
    """
    logger.debug(f"Rounding '{digit}' to the mathematical integer value.")
    return round(digit + 10 ** (-9))


def hpa_to_mm_hg_converter(pressure_in_hpa):
    """Converts pressure in hPa to mmHg (1 hPa = 0.75006 mm Hg)"""
    logger.debug(f"Converting pressure in hPa '{pressure_in_hpa}' to mmHg value.")
    return math_round(int(pressure_in_hpa) * 0.75006)
