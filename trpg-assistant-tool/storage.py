import json
import os

NPC_FILE = "npc_data.json"

def load_npcs():
    if os.path.exists(NPC_FILE):
        with open(NPC_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_npcs(npcs):
    with open(NPC_FILE, "w", encoding="utf-8") as file:
        json.dump(npcs, file, ensure_ascii=False, indent=4)
