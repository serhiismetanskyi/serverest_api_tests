import json
from pathlib import Path

BASE_PATH = Path.cwd() / "tests" / "data"


class FileManager:

    @staticmethod
    def read_file(file_name: str) -> dict:
        file_path = FileManager.get_file_with_json_ext(file_name)
        with open(file_path, mode="r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def update_file(file_name, data):
        file_path = FileManager.get_file_with_json_ext(file_name)
        with open(file_path, mode="r", encoding="utf-8") as file:
            json_data = json.load(file)
        json_data.update(data)
        with open(file_path, mode="w") as file:
            json.dump(json_data, file, indent=4)

    @staticmethod
    def clear_file(file_name):
        file_path = FileManager.get_file_with_json_ext(file_name)
        json_data = {}
        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)

    @staticmethod
    def get_file_with_json_ext(file_name: str) -> Path:
        if not file_name.endswith(".json"):
            file_name += ".json"
        return BASE_PATH / file_name
