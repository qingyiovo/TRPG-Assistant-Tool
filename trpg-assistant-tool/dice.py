import random

def roll_dice(dice_text):
    parts = dice_text.lower().split("d")

    if len(parts) != 2:
        raise ValueError("Invalid dice format")

    dice_count = int(parts[0])
    dice_sides = int(parts[1])

    results = []

    for i in range(dice_count):
        results.append(random.randint(1, dice_sides))

    return results, sum(results)
