import tkinter as tk
from tkinter import messagebox, Toplevel

from dice import roll_dice
from npc import create_npc, get_all_npcs, update_npc, delete_npc


class TRPGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRPG Keeper Studio")
        self.root.geometry("1000x700")

        self.selected_npc_index = None

        self.sidebar = tk.Frame(self.root, width=200, bg="#2b2b2b")
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg="#f5f5f5")
        self.content.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_dice_page()

    def create_sidebar(self):
        title = tk.Label(
            self.sidebar,
            text="TRPG Studio",
            font=("Arial", 18, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        title.pack(pady=25)

        self.create_sidebar_button("🎲 CoC Dice", self.show_dice_page)
        self.create_sidebar_button("👤 NPC Manager", self.show_npc_page)
        self.create_sidebar_button("📖 Clues", self.show_placeholder_page)
        self.create_sidebar_button("🗺 Maps", self.show_placeholder_page)
        self.create_sidebar_button("📅 Timeline", self.show_placeholder_page)
        self.create_sidebar_button("🎵 Music", self.show_placeholder_page)
        self.create_sidebar_button("📁 Campaign", self.show_placeholder_page)
        self.create_sidebar_button("⚙ Settings", self.show_placeholder_page)

    def create_sidebar_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text=text,
            width=18,
            height=2,
            command=command,
            bg="#3c3c3c",
            fg="white",
            relief="flat"
        )
        button.pack(pady=5)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_page_title(self, text):
        title = tk.Label(
            self.content,
            text=text,
            font=("Arial", 22, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=15)

    def show_dice_page(self):
        self.clear_content()
        self.create_page_title("CoC Dice Roller")

        frame = tk.Frame(self.content, bg="#f5f5f5")
        frame.pack(pady=20)

        tk.Label(frame, text="Dice Format:", bg="#f5f5f5").grid(row=0, column=0, padx=10)

        self.dice_entry = tk.Entry(frame, width=30)
        self.dice_entry.grid(row=0, column=1, padx=10)
        self.dice_entry.insert(0, "1d100")

        tk.Button(frame, text="Roll Dice", command=self.handle_roll_dice).grid(
            row=1, column=0, columnspan=2, pady=15
        )

        self.dice_result = tk.Label(
            self.content,
            text="Result will appear here.",
            font=("Arial", 14),
            bg="#f5f5f5"
        )
        self.dice_result.pack(pady=20)

    def handle_roll_dice(self):
        try:
            results, total = roll_dice(self.dice_entry.get())
            self.dice_result.config(text=f"Results: {results}\nTotal: {total}")
        except:
            messagebox.showerror("Error", "Please enter dice format like 1d100 or 2d6.")

    def show_npc_page(self):
        self.clear_content()
        self.selected_npc_index = None
        self.create_page_title("COC7 NPC Manager")

        main_frame = tk.Frame(self.content, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(side="left", fill="y", padx=10)

        list_frame = tk.Frame(main_frame, bg="#f5f5f5")
        list_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.entries = {}

        self.create_section_title(form_frame, "Basic Info", 0)
        self.create_input(form_frame, "Name", 1)
        self.create_input(form_frame, "Age", 2)
        self.create_input(form_frame, "Gender", 3)
        self.create_input(form_frame, "Occupation", 4)
        self.create_input(form_frame, "Role", 5)
        self.create_input(form_frame, "Portrait", 6)

        self.create_section_title(form_frame, "Attributes", 7)
        attributes = ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU"]
        row = 8
        for attr in attributes:
            self.create_input(form_frame, attr, row, default="50")
            row += 1

        self.create_section_title(form_frame, "Status", row)
        row += 1
        for status in ["HP", "MP", "SAN", "Luck"]:
            self.create_input(form_frame, status, row, default="50")
            row += 1

        self.create_section_title(form_frame, "Notes", row)
        row += 1
        self.create_input(form_frame, "Skills", row)
        row += 1
        self.create_input(form_frame, "Weapons", row)
        row += 1
        self.create_input(form_frame, "Background", row)
        row += 1
        self.create_input(form_frame, "Note", row)

        button_frame = tk.Frame(form_frame, bg="#f5f5f5")
        button_frame.grid(row=row + 1, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Save New NPC", command=self.handle_save_npc).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.handle_update_npc).grid(row=0, column=1, padx=5)

        tk.Label(
            list_frame,
            text="NPC List",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        ).pack(pady=5)

        self.npc_listbox = tk.Listbox(list_frame, height=24)
        self.npc_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.npc_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.npc_listbox.yview)

        self.npc_listbox.bind("<<ListboxSelect>>", self.handle_select_npc)
        self.npc_listbox.bind("<Double-Button-1>", self.open_npc_detail_window)

        action_frame = tk.Frame(self.content, bg="#f5f5f5")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="View Detail", command=self.open_npc_detail_window).grid(row=0, column=0, padx=10)
        tk.Button(action_frame, text="Delete Selected NPC", command=self.handle_delete_npc).grid(row=0, column=1, padx=10)

        self.refresh_npc_list()

    def create_section_title(self, parent, text, row):
        label = tk.Label(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        )
        label.grid(row=row, column=0, columnspan=2, pady=(10, 3), sticky="w")

    def create_input(self, parent, label_text, row, default=""):
        tk.Label(parent, text=label_text, bg="#f5f5f5").grid(
            row=row, column=0, padx=5, pady=2, sticky="e"
        )

        entry = tk.Entry(parent, width=32)
        entry.grid(row=row, column=1, padx=5, pady=2)

        if default:
            entry.insert(0, default)

        self.entries[label_text] = entry

    def get_form_data(self):
        return {
            "basic_info": {
                "name": self.entries["Name"].get(),
                "age": self.entries["Age"].get(),
                "gender": self.entries["Gender"].get(),
                "occupation": self.entries["Occupation"].get(),
                "role": self.entries["Role"].get(),
                "portrait": self.entries["Portrait"].get()
            },
            "attributes": {
                "STR": self.entries["STR"].get(),
                "CON": self.entries["CON"].get(),
                "SIZ": self.entries["SIZ"].get(),
                "DEX": self.entries["DEX"].get(),
                "APP": self.entries["APP"].get(),
                "INT": self.entries["INT"].get(),
                "POW": self.entries["POW"].get(),
                "EDU": self.entries["EDU"].get()
            },
            "status": {
                "HP": self.entries["HP"].get(),
                "MP": self.entries["MP"].get(),
                "SAN": self.entries["SAN"].get(),
                "Luck": self.entries["Luck"].get()
            },
            "details": {
                "skills": self.entries["Skills"].get(),
                "weapons": self.entries["Weapons"].get(),
                "background": self.entries["Background"].get(),
                "note": self.entries["Note"].get()
            }
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        for key in ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU", "HP", "MP", "SAN", "Luck"]:
            self.entries[key].insert(0, "50")

    def fill_form(self, npc):
        self.clear_form()

        basic = npc.get("basic_info", {})
        attributes = npc.get("attributes", {})
        status = npc.get("status", {})
        details = npc.get("details", {})

        values = {
            "Name": basic.get("name", ""),
            "Age": basic.get("age", ""),
            "Gender": basic.get("gender", ""),
            "Occupation": basic.get("occupation", ""),
            "Role": basic.get("role", ""),
            "Portrait": basic.get("portrait", ""),

            "STR": attributes.get("STR", "50"),
            "CON": attributes.get("CON", "50"),
            "SIZ": attributes.get("SIZ", "50"),
            "DEX": attributes.get("DEX", "50"),
            "APP": attributes.get("APP", "50"),
            "INT": attributes.get("INT", "50"),
            "POW": attributes.get("POW", "50"),
            "EDU": attributes.get("EDU", "50"),

            "HP": status.get("HP", "50"),
            "MP": status.get("MP", "50"),
            "SAN": status.get("SAN", "50"),
            "Luck": status.get("Luck", "50"),

            "Skills": details.get("skills", ""),
            "Weapons": details.get("weapons", ""),
            "Background": details.get("background", ""),
            "Note": details.get("note", "")
        }

        for key, value in values.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def handle_save_npc(self):
        data = self.get_form_data()

        if not data["basic_info"]["name"]:
            messagebox.showerror("Error", "NPC name cannot be empty.")
            return

        create_npc(data)
        messagebox.showinfo("Success", "NPC saved successfully.")
        self.clear_form()
        self.refresh_npc_list()

    def handle_update_npc(self):
        if self.selected_npc_index is None:
            messagebox.showerror("Error", "Please select an NPC first.")
            return

        data = self.get_form_data()
        success = update_npc(self.selected_npc_index, data)

        if success:
            messagebox.showinfo("Success", "NPC updated successfully.")
            self.refresh_npc_list()
        else:
            messagebox.showerror("Error", "Update failed.")

    def refresh_npc_list(self):
        self.npc_listbox.delete(0, tk.END)

        npcs = get_all_npcs()

        if not npcs:
            self.npc_listbox.insert(tk.END, "No NPC data.")
            return

        for index, npc in enumerate(npcs, start=1):
            basic = npc.get("basic_info", {})
            name = basic.get("name", "")
            occupation = basic.get("occupation", "")
            role = basic.get("role", "")
            self.npc_listbox.insert(tk.END, f"{index}. {name} | {occupation} | {role}")

    def handle_select_npc(self, event=None):
        selected = self.npc_listbox.curselection()

        if not selected:
            return

        index = selected[0]
        npcs = get_all_npcs()

        if index >= len(npcs):
            return

        self.selected_npc_index = index
        self.fill_form(npcs[index])

    def handle_delete_npc(self):
        if self.selected_npc_index is None:
            messagebox.showerror("Error", "Please select an NPC first.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this NPC?")

        if confirm:
            success = delete_npc(self.selected_npc_index)

            if success:
                messagebox.showinfo("Success", "NPC deleted successfully.")
                self.selected_npc_index = None
                self.clear_form()
                self.refresh_npc_list()
            else:
                messagebox.showerror("Error", "Delete failed.")

    def open_npc_detail_window(self, event=None):
        if self.selected_npc_index is None:
            messagebox.showerror("Error", "Please select an NPC first.")
            return

        npcs = get_all_npcs()

        if self.selected_npc_index >= len(npcs):
            return

        npc = npcs[self.selected_npc_index]

        basic = npc.get("basic_info", {})
        attributes = npc.get("attributes", {})
        status = npc.get("status", {})
        details = npc.get("details", {})

        window = Toplevel(self.root)
        window.title(f"NPC Detail - {basic.get('name', '')}")
        window.geometry("500x600")

        detail_text = f"""
Name: {basic.get('name', '')}
Age: {basic.get('age', '')}
Gender: {basic.get('gender', '')}
Occupation: {basic.get('occupation', '')}
Role: {basic.get('role', '')}
Portrait: {basic.get('portrait', '')}

Attributes
STR: {attributes.get('STR', '')}
CON: {attributes.get('CON', '')}
SIZ: {attributes.get('SIZ', '')}
DEX: {attributes.get('DEX', '')}
APP: {attributes.get('APP', '')}
INT: {attributes.get('INT', '')}
POW: {attributes.get('POW', '')}
EDU: {attributes.get('EDU', '')}

Status
HP: {status.get('HP', '')}
MP: {status.get('MP', '')}
SAN: {status.get('SAN', '')}
Luck: {status.get('Luck', '')}

Skills:
{details.get('skills', '')}

Weapons:
{details.get('weapons', '')}

Background:
{details.get('background', '')}

Note:
{details.get('note', '')}
"""

        tk.Label(
            window,
            text=detail_text,
            justify="left",
            font=("Arial", 11),
            padx=20,
            pady=20
        ).pack(anchor="w")

    def show_placeholder_page(self):
        self.clear_content()
        self.create_page_title("Coming Soon")

        tk.Label(
            self.content,
            text="This feature will be added in a future version.",
            font=("Arial", 14),
            bg="#f5f5f5"
        ).pack(pady=20)

    def run(self):
        self.root.mainloop()
