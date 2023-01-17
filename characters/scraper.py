from sqlite3 import IntegrityError

import requests

from characters.models import Character
from rick_and_morty_api.settings import RICK_AND_MORTY_CHARACTER_URL


def scrape_character() -> list[Character]:
    next_character_to_scrape = RICK_AND_MORTY_CHARACTER_URL

    characters = []

    while next_character_to_scrape is not None:
        character_resp = requests.get(next_character_to_scrape).json()

        for character in character_resp["results"]:
            characters.append(
                Character(
                    name=character["name"],
                    api_id=character["id"],
                    status=character["status"],
                    species=character["species"],
                    gender=character["gender"],
                    image=character["image"],
                )
            )
        next_character_to_scrape = character_resp["info"]["next"]
    return characters


def save_characters(characters: list[Character]) -> None:
    for character in characters:
        try:
            character.save()
        except IntegrityError:
            print(f"This character {character} exist!")


def sync_characters_with_api() -> None:
    characters = scrape_character()
    save_characters(characters)
