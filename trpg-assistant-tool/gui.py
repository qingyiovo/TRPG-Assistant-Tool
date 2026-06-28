import tkinter as tk
from tkinter import messagebox

from dice import roll_dice
from npc import add_npc, get_all_npcs


class TRPGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRPG Assistant Tool")
        self.root.geometry("800x500")

        self.sidebar = tk.Frame(self.root, width=180)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root)
        self.content.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_dice_page()

    def create_sidebar(self):
        title = tk.Label(self.sidebar, text="TRPG Tool", font=("Arial", 16))
        title.pack(pady=20)

        dice_button = tk.Button(
            self.sidebar,
            text="Dice",
            width=18,
            command=self.show_dice_page
        )
        dice_button.pack(pady=5)

        npc_button = tk.Button(
            self.sidebar,
            text="NPC Manager",
            width=18,
            command=self.show_npc_page
        )
        npc_button.pack(pady=5)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dice_page(self):
        self.clear_content()

        title = tk.Label(self.content, text="Dice Roller", font=("Arial", 18))
        title.pack(pady=20)

        self.dice_entry = tk.Entry(self.content, width=30)
        self.dice_entry.pack(pady=10)
        self.dice_entry.insert(0, "1d100")

        roll_button = tk.Button(
            self.content,
            text="Roll Dice",
            command=self.handle_roll_dice
        )
        roll_button.pack(pady=10)

        self.dice_result = tk.Label(self.content, text="Result will appear here.")
        self.dice_result.pack(pady=20)

    def handle_roll_dice(self):
        try:
            dice_text = self.dice_entry.get()
            results, total = roll_dice(dice_text)
            self.dice_result.config(text=f"Results: {results}\nTotal: {total}")
        except:
            messagebox.showerror("Error", "Please enter dice format like 1d100 or 2d6.")

    def show_npc_page(self):
        self.clear_content()

        title = tk.Label(self.content, text="NPC Manager", font=("Arial", 18))
        title.pack(pady=10)

        self.name_entry = self.create_input("Name")
        self.age_entry = self.create_input("Age")
        self.occupation_entry = self.create_input("Occupation")
        self.role_entry = self.create_input("Role")
        self.note_entry = self.create_input("Note")

        save_button = tk.Button(
            self.content,
            text="Save NPC",
            command=self.handle_save_npc
        )
        save_button.pack(pady=10)

        self.npc_list_label = tk.Label(self.content, text="")
        self.npc_list_label.pack(pady=10)

        self.refresh_npc_list()

    def create_input(self, label_text):
        label = tk.Label(self.content, text=label_text)
        label.pack()

        entry = tk.Entry(self.content, width=40)
        entry.pack(pady=3)

        return entry

    def handle_save_npc(self):
        add_npc(
            self.name_entry.get(),
            self.age_entry.get(),
            self.occupation_entry.get(),
            self.role_entry.get(),
            self.note_entry.get()
        )

        messagebox.showinfo("Success", "NPC saved successfully.")
        self.show_npc_page()

    def refresh_npc_list(self):
        npcs = get_all_npcs()

        if not npcs:
            self.npc_list_label.config(text="No NPC data.")
            return

        text = "NPC List:\n\n"

        for index, npc in enumerate(npcs, start=1):
            text += f"{index}. {npc['name']} - {npc['occupation']} - {npc['role']}\n"

        self.npc_list_label.config(text=text)

    def run(self):
        self.root.mainloop()
