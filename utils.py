"""Module contains useful tools"""


def math_round(digit):
    """Performs mathematical rounding e.g. 0.4 -> 0, 1.5 -> 2
    input  [0.4, 0.5, 0.1, 1.2, 1.4, 1.5, 9.19, 13.1]
    output [0, 1, 0, 1, 1, 2, 10, 13]
    """
    return round(digit + 10 ** (-9))


def hpa_to_mm_hg_converter(pressure_in_hpa):
    """Converts pressure in hPa to mmHg (1 hPa = 0.75006 mm Hg)"""
    return math_round(int(pressure_in_hpa) * 0.75006)
