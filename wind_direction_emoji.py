WIND_DIRECTION_EMOJI = {
    "\U00002B06": [(338, 360), (0, 23)],
    "\U00002197": [(23, 68)],
    "\U000027A1": [(68, 113)],
    "\U00002198": [(113, 158)],
    "\U00002B07": [(158, 203)],
    "\U00002199": [(203, 248)],
    "\U00002B05": [(248, 293)],
    "\U00002196": [(293, 338)]
}


def check_presense(wind_direction, degree_range):
    if wind_direction in range(*degree_range):
        return True
    return False


def get_wind_direction_emoji(wind_direction):
    if wind_direction is None:
        return "\U0000262F"
    for key, value in WIND_DIRECTION_EMOJI.items():
        result = []
        for item in value:
            result.append(check_presense(wind_direction=wind_direction, degree_range=item))
        if any(result):
            return key
    return "\U0000262F"
