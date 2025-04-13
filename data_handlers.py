import json
from pathlib import Path
from config import DATA_FILE, REMINDER_FILE

def read_message() -> str:
    """Read the message from the reminder file."""
    try:
        return Path(REMINDER_FILE).read_text()
    except FileNotFoundError:
        return "The file was not found."
    except IOError:
        return "An error occurred while reading the file."

def read_json_data() -> dict:
    """Read and parse the JSON data file."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        print("JSON data has been read back from the file.")
        return data
    except FileNotFoundError:
        print(f"Data file {DATA_FILE} not found. Creating new file.")
        return []

def write_json_data(data: dict) -> None:
    """Write data to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print(f"JSON data has been written to {DATA_FILE}.")