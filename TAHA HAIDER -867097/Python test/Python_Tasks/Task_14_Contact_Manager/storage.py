import json
import os


def load_contacts():

    if not os.path.exists("contacts.json"):
        return []

    try:
        with open("contacts.json", "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        raise ValueError("JSON file is corrupted")


def save_contacts(contacts):

    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)
