from storage import load_clues, save_clues


def create_clue(data):
    clues = load_clues()
    clues.append(data)
    save_clues(clues)


def get_all_clues():
    return load_clues()


def update_clue(index, data):
    clues = load_clues()

    if index < 0 or index >= len(clues):
        return False

    clues[index] = data
    save_clues(clues)
    return True


def delete_clue(index):
    clues = load_clues()

    if index < 0 or index >= len(clues):
        return False

    clues.pop(index)
    save_clues(clues)
    return True


def search_clues(keyword):
    clues = load_clues()
    keyword = keyword.lower()

    results = []

    for index, clue in enumerate(clues):
        title = clue.get("title", "").lower()
        description = clue.get("description", "").lower()
        location = clue.get("location", "").lower()
        related_npc = clue.get("related_npc", "").lower()
        tags = clue.get("tags", "").lower()

        if (
            keyword in title
            or keyword in description
            or keyword in location
            or keyword in related_npc
            or keyword in tags
        ):
            results.append((index, clue))

    return results
