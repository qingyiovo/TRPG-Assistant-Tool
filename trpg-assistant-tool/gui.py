import tkinter as tk
from tkinter import messagebox, Toplevel, ttk, filedialog

from dice import roll_dice
from npc import create_npc, get_all_npcs, update_npc, delete_npc


class TRPGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRPG Keeper Studio")
        self.root.geometry("1100x750")

        self.selected_npc_index = None
        self.entries = {}

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
        self.entries = {}

        self.create_page_title("COC7 NPC Manager")

        main_frame = tk.Frame(self.content, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        left_frame = tk.Frame(main_frame, bg="#f5f5f5")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        right_frame = tk.Frame(main_frame, bg="#f5f5f5")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill="both", expand=True)

        basic_tab = tk.Frame(notebook, bg="#f5f5f5")
        attr_tab = tk.Frame(notebook, bg="#f5f5f5")
        combat_tab = tk.Frame(notebook, bg="#f5f5f5")
        skills_tab = tk.Frame(notebook, bg="#f5f5f5")
        notes_tab = tk.Frame(notebook, bg="#f5f5f5")

        notebook.add(basic_tab, text="Basic")
        notebook.add(attr_tab, text="Attributes")
        notebook.add(combat_tab, text="Combat")
        notebook.add(skills_tab, text="Skills")
        notebook.add(notes_tab, text="Notes")

        self.create_input(basic_tab, "Name", 0)
        self.create_input(basic_tab, "Age", 1)
        self.create_input(basic_tab, "Gender", 2)
        self.create_input(basic_tab, "Occupation", 3)
        self.create_input(basic_tab, "Role", 4)
        self.create_input(basic_tab, "Portrait", 5)

        tk.Button(
            basic_tab,
            text="Select Image",
            command=self.select_portrait
        ).grid(row=6, column=1, pady=10, sticky="w")

        attributes = ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU"]
        for i, attr in enumerate(attributes):
            self.create_input(attr_tab, attr, i, default="50")

        status_fields = ["HP", "MP", "SAN", "Luck", "Move", "Build", "Damage Bonus"]
        for i, field in enumerate(status_fields):
            self.create_input(combat_tab, field, i, default="")

        combat_fields = ["Weapons", "Dodge", "Fighting"]
        for i, field in enumerate(combat_fields, start=len(status_fields)):
            self.create_input(combat_tab, field, i)

        skills = [
            "Spot Hidden",
            "Listen",
            "Psychology",
            "Library Use",
            "Stealth",
            "Persuade",
            "Fast Talk",
            "Intimidate",
            "Medicine",
            "Occult"
        ]

        for i, skill in enumerate(skills):
            self.create_input(skills_tab, skill, i, default="")

        note_fields = [
            "Backstory",
            "Ideology",
            "Significant Person",
            "Treasured Possession",
            "Trait",
            "Note"
        ]

        for i, field in enumerate(note_fields):
            self.create_input(notes_tab, field, i)

        button_frame = tk.Frame(left_frame, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save New NPC", command=self.handle_save_npc).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.handle_update_npc).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form).grid(row=0, column=2, padx=5)

        tk.Label(
            right_frame,
            text="NPC List",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        ).pack(pady=5)

        self.npc_listbox = tk.Listbox(right_frame, height=25)
        self.npc_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(right_frame)
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

    def create_input(self, parent, label_text, row, default=""):
        tk.Label(parent, text=label_text, bg="#f5f5f5").grid(
            row=row, column=0, padx=8, pady=5, sticky="e"
        )

        entry = tk.Entry(parent, width=35)
        entry.grid(row=row, column=1, padx=8, pady=5)

        if default:
            entry.insert(0, default)

        self.entries[label_text] = entry

    def select_portrait(self):
        file_path = filedialog.askopenfilename(
            title="Select NPC Portrait",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.entries["Portrait"].delete(0, tk.END)
            self.entries["Portrait"].insert(0, file_path)

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
                "Luck": self.entries["Luck"].get(),
                "Move": self.entries["Move"].get(),
                "Build": self.entries["Build"].get(),
                "Damage Bonus": self.entries["Damage Bonus"].get()
            },
            "combat": {
                "Weapons": self.entries["Weapons"].get(),
                "Dodge": self.entries["Dodge"].get(),
                "Fighting": self.entries["Fighting"].get()
            },
            "skills": {
                "Spot Hidden": self.entries["Spot Hidden"].get(),
                "Listen": self.entries["Listen"].get(),
                "Psychology": self.entries["Psychology"].get(),
                "Library Use": self.entries["Library Use"].get(),
                "Stealth": self.entries["Stealth"].get(),
                "Persuade": self.entries["Persuade"].get(),
                "Fast Talk": self.entries["Fast Talk"].get(),
                "Intimidate": self.entries["Intimidate"].get(),
                "Medicine": self.entries["Medicine"].get(),
                "Occult": self.entries["Occult"].get()
            },
            "background": {
                "Backstory": self.entries["Backstory"].get(),
                "Ideology": self.entries["Ideology"].get(),
                "Significant Person": self.entries["Significant Person"].get(),
                "Treasured Possession": self.entries["Treasured Possession"].get(),
                "Trait": self.entries["Trait"].get(),
                "Note": self.entries["Note"].get()
            }
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        for key in ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU"]:
            self.entries[key].insert(0, "50")

    def fill_form(self, npc):
        self.clear_form()

        sections = {
            **npc.get("basic_info", {}),
            **npc.get("attributes", {}),
            **npc.get("status", {}),
            **npc.get("combat", {}),
            **npc.get("skills", {}),
            **npc.get("background", {})
        }

        key_map = {
            "name": "Name",
            "age": "Age",
            "gender": "Gender",
            "occupation": "Occupation",
            "role": "Role",
            "portrait": "Portrait"
        }

        for key, value in sections.items():
            field_name = key_map.get(key, key)

            if field_name in self.entries:
                self.entries[field_name].delete(0, tk.END)
                self.entries[field_name].insert(0, value)

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

        window = Toplevel(self.root)
        window.title("NPC Detail")
        window.geometry("600x700")

        text_box = tk.Text(window, wrap="word", font=("Arial", 11))
        text_box.pack(fill="both", expand=True, padx=15, pady=15)

        detail_text = self.format_npc_detail(npc)
        text_box.insert("1.0", detail_text)
        text_box.config(state="disabled")

    def format_npc_detail(self, npc):
        basic = npc.get("basic_info", {})
        attributes = npc.get("attributes", {})
        status = npc.get("status", {})
        combat = npc.get("combat", {})
        skills = npc.get("skills", {})
        background = npc.get("background", {})

        text = "=== Basic Information ===\n"
        for key, value in basic.items():
            text += f"{key}: {value}\n"

        text += "\n=== Attributes ===\n"
        for key, value in attributes.items():
            text += f"{key}: {value}\n"

        text += "\n=== Status ===\n"
        for key, value in status.items():
            text += f"{key}: {value}\n"

        text += "\n=== Combat ===\n"
        for key, value in combat.items():
            text += f"{key}: {value}\n"

        text += "\n=== Skills ===\n"
        for key, value in skills.items():
            text += f"{key}: {value}\n"

        text += "\n=== Background ===\n"
        for key, value in background.items():
            text += f"{key}: {value}\n"

        return text

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
