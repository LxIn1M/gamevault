import os

import requests


STEAM_API_BASE_URL = "https://api.steampowered.com"


class SteamAPIError(Exception):
    pass


def get_steam_api_key():
    api_key = os.getenv("STEAM_API_KEY")

    if not api_key:
        raise SteamAPIError(
            "STEAM_API_KEY is missing from the .env file."
        )

    return api_key


def get_owned_games(steam_id):
    url = (
        f"{STEAM_API_BASE_URL}"
        "/IPlayerService/GetOwnedGames/v1/"
    )

    params = {
        "key": get_steam_api_key(),
        "steamid": steam_id,
        "include_appinfo": "true",
        "include_played_free_games": "true",
        "format": "json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise SteamAPIError(
            "Could not connect to Steam."
        ) from error

    data = response.json()

    steam_response = data.get("response", {})

    if "game_count" not in steam_response:
        raise SteamAPIError(
            "Steam library is unavailable. "
            "Make sure Game details are public."
        )

    return steam_response.get("games", [])


def get_player_summary(steam_id):
    url = (
        f"{STEAM_API_BASE_URL}"
        "/ISteamUser/GetPlayerSummaries/v2/"
    )

    params = {
        "key": get_steam_api_key(),
        "steamids": steam_id,
        "format": "json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise SteamAPIError(
            "Could not retrieve Steam profile."
        ) from error

    data = response.json()

    players = (
        data
        .get("response", {})
        .get("players", [])
    )

    if not players:
        raise SteamAPIError(
            "Steam profile was not found."
        )

    return players[0]


def get_steam_header_image(app_id):
    return (
        "https://cdn.akamai.steamstatic.com/"
        f"steam/apps/{app_id}/header.jpg"
    )