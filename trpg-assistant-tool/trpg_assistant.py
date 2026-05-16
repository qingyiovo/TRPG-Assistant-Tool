import random
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


def roll_dice():
    dice_text = input("Enter dice format, for example 1d100 or 2d6: ")

    try:
        parts = dice_text.lower().split("d")
        dice_count = int(parts[0])
        dice_sides = int(parts[1])

        results = []
        for i in range(dice_count):
            results.append(random.randint(1, dice_sides))

        total = sum(results)

        print("Roll results:", results)
        print("Total:", total)

    except:
        print("Invalid input. Please use format like 1d100, 2d6, 3d10.")


def add_npc():
    print("\n===== Add NPC =====")

    npc = {
        "basic_info": {
            "name": input("姓名 Name: "),
            "age": input("年龄 Age: "),
            "gender": input("性别 Gender: "),
            "occupation": input("职业 Occupation: "),
            "role": input("身份/剧情定位 Role: "),
            "note": input("KP备注 Note: ")
        },
        "attributes": {
            "STR": int(input("力量 STR: ")),
            "CON": int(input("体质 CON: ")),
            "SIZ": int(input("体型 SIZ: ")),
            "DEX": int(input("敏捷 DEX: ")),
            "APP": int(input("外貌 APP: ")),
            "INT": int(input("智力 INT: ")),
            "POW": int(input("意志 POW: ")),
            "EDU": int(input("教育 EDU: "))
        },
        "status": {
            "HP": int(input("HP: ")),
            "SAN": int(input("SAN: ")),
            "MP": int(input("MP: ")),
            "LUCK": int(input("幸运 LUCK: ")),
            "MOV": int(input("移动 MOV: ")),
            "DB": input("伤害加值 DB: "),
            "BUILD": input("体格 Build: "),
            "Armor": input("护甲 Armor: ")
        },
        "skills": {},
        "weapons": [],
        "background": {
            "description": input("外貌描述 Description: "),
            "belief": input("信念 Belief: "),
            "important_people": input("重要之人 Important People: "),
            "important_place": input("重要地点 Important Place: "),
            "treasure": input("宝物 Treasure: "),
            "trait": input("特质 Trait: "),
            "fear": input("恐惧 Fear: "),
            "story": input("背景故事 Story: ")
        }
    }

    print("\n输入技能，输入 done 结束。")
    while True:
        skill_name = input("技能名 Skill Name: ")
        if skill_name.lower() == "done":
            break
        skill_value = int(input("技能数值 Skill Value: "))
        npc["skills"][skill_name] = skill_value

    print("\n输入武器，输入 done 结束。")
    while True:
        weapon_name = input("武器名 Weapon Name: ")
        if weapon_name.lower() == "done":
            break

        npc["weapons"].append({
            "name": weapon_name,
            "damage": input("伤害 Damage: "),
            "range": input("射程 Range: "),
            "attacks": input("攻击次数 Attacks: ")
        })

    npcs = load_npcs()
    npcs.append(npc)
    save_npcs(npcs)

    print("\nNPC saved successfully!")


def view_npcs():
    npcs = load_npcs()

    if not npcs:
        print("\nNo NPC data found.")
        return

    print("\n===== NPC List =====")

    for index, npc in enumerate(npcs, start=1):
        info = npc["basic_info"]
        status = npc["status"]

        print(f"\n[{index}] {info['name']}")
        print(f"Role: {info['role']}")
        print(f"Occupation: {info['occupation']}")
        print(f"HP: {status['HP']} / SAN: {status['SAN']} / MP: {status['MP']}")
        print(f"Note: {info['note']}")


def main():
    while True:
        print("\n===== TRPG Assistant Tool =====")
        print("1. Roll Dice")
        print("2. Add NPC")
        print("3. View NPC List")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            roll_dice()
        elif choice == "2":
            add_npc()
        elif choice == "3":
            view_npcs()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, 3, or 4.")


main()