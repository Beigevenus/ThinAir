import json
from json import JSONDecodeError
from typing import Optional


class JsonHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> Optional[dict]:
        """
        Loads the JSON file into a dictionary.

        :return: A dictionary symbolizing the JSON file, or None if it cannot be parsed or doesn't exist
        """
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (JSONDecodeError, FileNotFoundError):
            return None

    def write(self, dictionary: dict) -> None:
        """
        Writes the given dictionary a JSON file.

        :param dictionary: The dictionary to write to a JSON file
        """
        with open(self.filepath, "w") as file:
            json.dump(dictionary, file)
