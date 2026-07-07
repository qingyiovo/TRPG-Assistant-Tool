import random


def roll_dice(dice_text):
    dice_text = dice_text.lower().strip()

    if "d" not in dice_text:
        raise ValueError("Invalid dice format")

    parts = dice_text.split("d")

    if len(parts) != 2:
        raise ValueError("Invalid dice format")

    dice_count_text = parts[0]
    dice_sides_text = parts[1]

    if dice_count_text == "":
        dice_count = 1
    else:
        dice_count = int(dice_count_text)

    dice_sides = int(dice_sides_text)

    if dice_count <= 0 or dice_sides <= 0:
        raise ValueError("Dice count and sides must be positive")

    results = []

    for i in range(dice_count):
        results.append(random.randint(1, dice_sides))

    return results, sum(results)


def check_skill_success(skill_value, roll_result):
    skill_value = int(skill_value)
    roll_result = int(roll_result)

    if skill_value < 1 or skill_value > 100:
        raise ValueError("Skill value must be between 1 and 100")

    if roll_result < 1 or roll_result > 100:
        raise ValueError("Roll result must be between 1 and 100")

    extreme_success = skill_value // 5
    hard_success = skill_value // 2

    if roll_result == 1:
        return "Critical Success"

    if roll_result <= extreme_success:
        return "Extreme Success"

    if roll_result <= hard_success:
        return "Hard Success"

    if roll_result <= skill_value:
        return "Regular Success"

    if skill_value < 50 and roll_result >= 96:
        return "Fumble"

    if skill_value >= 50 and roll_result == 100:
        return "Fumble"

    return "Failure"


def roll_coc_skill_check(skill_value):
    roll_result = random.randint(1, 100)
    success_level = check_skill_success(skill_value, roll_result)

    return roll_result, success_level
