import json
import os

DATA_DIR = "data"
NPC_FILE = os.path.join(DATA_DIR, "npc_data.json")
CLUE_FILE = os.path.join(DATA_DIR, "clue_data.json")


def ensure_data_folder():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_json(file_path):
    ensure_data_folder()

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    return []


def save_json(file_path, data):
    ensure_data_folder()

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_npcs():
    return load_json(NPC_FILE)


def save_npcs(npcs):
    save_json(NPC_FILE, npcs)


def load_clues():
    return load_json(CLUE_FILE)


def save_clues(clues):
    save_json(CLUE_FILE, clues)
