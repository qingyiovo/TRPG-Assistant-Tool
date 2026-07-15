import tkinter as tk
from tkinter import messagebox, Toplevel, ttk, filedialog

from dice import roll_dice, roll_coc_with_bonus_or_penalty, roll_san_check
from npc import create_npc, get_all_npcs, update_npc, delete_npc
from clues import create_clue, get_all_clues, update_clue, delete_clue, search_clues
from campaigns import create_campaign, get_all_campaigns, update_campaign, delete_campaign


class TRPGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRPG Keeper Studio")
        self.root.geometry("1150x760")

        self.selected_npc_index = None
        self.selected_clue_index = None
        self.selected_campaign_index = None

        self.npc_entries = {}
        self.clue_entries = {}
        self.campaign_entries = {}

        self.sidebar = tk.Frame(self.root, width=210, bg="#2b2b2b")
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg="#f5f5f5")
        self.content.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_dice_page()

    # ======================
    # Basic Layout
    # ======================

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
        self.create_sidebar_button("📖 Clues", self.show_clues_page)
        self.create_sidebar_button("📁 Campaign", self.show_campaign_page)
        self.create_sidebar_button("🗺 Maps", self.show_maps_page)
        self.create_sidebar_button("📅 Timeline", self.show_timeline_page)
        self.create_sidebar_button("🎵 Music", self.show_music_page)
        self.create_sidebar_button("⚙ Settings", self.show_settings_page)

    def create_sidebar_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text=text,
            width=20,
            height=2,
            command=command,
            bg="#3c3c3c",
            fg="white",
            relief="flat",
            anchor="w",
            padx=15
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

    # ======================
    # Dice System
    # ======================

    def show_dice_page(self):
        self.clear_content()
        self.create_page_title("COC7 Dice System")

        main_frame = tk.Frame(self.content, bg="#f5f5f5")
        main_frame.pack(pady=10)

        normal_frame = tk.LabelFrame(
            main_frame,
            text="Normal Dice Roller",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            padx=20,
            pady=15
        )
        normal_frame.pack(pady=10, fill="x")

        tk.Label(normal_frame, text="Dice Format:", bg="#f5f5f5").grid(
            row=0, column=0, padx=10, pady=8
        )

        self.dice_entry = tk.Entry(normal_frame, width=30)
        self.dice_entry.grid(row=0, column=1, padx=10, pady=8)
        self.dice_entry.insert(0, "1d100")

        tk.Button(
            normal_frame,
            text="Roll Dice",
            command=self.handle_roll_dice
        ).grid(row=1, column=0, columnspan=2, pady=8)

        self.dice_result = tk.Label(
            normal_frame,
            text="Result will appear here.",
            font=("Arial", 12),
            bg="#f5f5f5",
            justify="left"
        )
        self.dice_result.grid(row=2, column=0, columnspan=2, pady=8)

        skill_frame = tk.LabelFrame(
            main_frame,
            text="COC7 Skill Check",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            padx=20,
            pady=15
        )
        skill_frame.pack(pady=10, fill="x")

        tk.Label(skill_frame, text="Skill Value:", bg="#f5f5f5").grid(
            row=0, column=0, padx=10, pady=8
        )

        self.skill_entry = tk.Entry(skill_frame, width=30)
        self.skill_entry.grid(row=0, column=1, padx=10, pady=8)
        self.skill_entry.insert(0, "60")

        tk.Button(
            skill_frame,
            text="Normal Check",
            command=lambda: self.handle_skill_check("normal")
        ).grid(row=1, column=0, padx=5, pady=8)

        tk.Button(
            skill_frame,
            text="Bonus Dice",
            command=lambda: self.handle_skill_check("bonus")
        ).grid(row=1, column=1, padx=5, pady=8)

        tk.Button(
            skill_frame,
            text="Penalty Dice",
            command=lambda: self.handle_skill_check("penalty")
        ).grid(row=1, column=2, padx=5, pady=8)

        self.skill_result = tk.Label(
            skill_frame,
            text="Skill check result will appear here.",
            font=("Arial", 12),
            bg="#f5f5f5",
            justify="left"
        )
        self.skill_result.grid(row=2, column=0, columnspan=3, pady=8)

        san_frame = tk.LabelFrame(
            main_frame,
            text="SAN Check",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            padx=20,
            pady=15
        )
        san_frame.pack(pady=10, fill="x")

        tk.Label(san_frame, text="SAN Value:", bg="#f5f5f5").grid(
            row=0, column=0, padx=10, pady=8
        )

        self.san_entry = tk.Entry(san_frame, width=20)
        self.san_entry.grid(row=0, column=1, padx=10, pady=8)
        self.san_entry.insert(0, "60")

        tk.Label(san_frame, text="Success Loss:", bg="#f5f5f5").grid(
            row=1, column=0, padx=10, pady=8
        )

        self.san_success_loss_entry = tk.Entry(san_frame, width=20)
        self.san_success_loss_entry.grid(row=1, column=1, padx=10, pady=8)
        self.san_success_loss_entry.insert(0, "0")

        tk.Label(san_frame, text="Failure Loss:", bg="#f5f5f5").grid(
            row=2, column=0, padx=10, pady=8
        )

        self.san_failure_loss_entry = tk.Entry(san_frame, width=20)
        self.san_failure_loss_entry.grid(row=2, column=1, padx=10, pady=8)
        self.san_failure_loss_entry.insert(0, "1d6")

        tk.Button(
            san_frame,
            text="Roll SAN Check",
            command=self.handle_san_check
        ).grid(row=3, column=0, columnspan=2, pady=8)

        self.san_result = tk.Label(
            san_frame,
            text="SAN check result will appear here.",
            font=("Arial", 12),
            bg="#f5f5f5",
            justify="left"
        )
        self.san_result.grid(row=4, column=0, columnspan=2, pady=8)

    def handle_roll_dice(self):
        try:
            dice_text = self.dice_entry.get()
            results, total = roll_dice(dice_text)

            self.dice_result.config(
                text=f"Dice: {dice_text}\nResults: {results}\nTotal: {total}"
            )
        except Exception:
            messagebox.showerror(
                "Error",
                "Please enter dice format like 1d100, d100, 2d6, or 3d10."
            )

    def handle_skill_check(self, mode):
        try:
            skill_value = int(self.skill_entry.get())
            result = roll_coc_with_bonus_or_penalty(skill_value, mode)

            self.skill_result.config(
                text=self.format_coc_check_result(result)
            )
        except Exception:
            messagebox.showerror(
                "Error",
                "Please enter a valid skill value between 1 and 100."
            )

    def format_coc_check_result(self, result):
        mode = result["mode"]

        if mode == "normal":
            mode_text = "Normal Check"
        elif mode == "bonus":
            mode_text = "Bonus Dice"
        elif mode == "penalty":
            mode_text = "Penalty Dice"
        else:
            mode_text = "Unknown"

        return (
            f"Check Type: {mode_text}\n"
            f"Skill Value: {result['skill_value']}\n"
            f"Tens Rolls: {result['tens_rolls']}\n"
            f"Ones Digit: {result['ones_digit']}\n"
            f"Final Roll: {result['roll_result']}\n"
            f"Result: {result['success_level']}"
        )

    def handle_san_check(self):
        try:
            result = roll_san_check(
                self.san_entry.get(),
                self.san_success_loss_entry.get(),
                self.san_failure_loss_entry.get()
            )

            self.san_result.config(
                text=(
                    f"SAN Value: {result['san_value']}\n"
                    f"Roll: {result['roll_result']}\n"
                    f"Result: {result['success_level']}\n"
                    f"Loss Rule: {result['loss_text']}\n"
                    f"Loss Detail: {result['loss_detail']}\n"
                    f"SAN Loss: {result['san_loss']}"
                )
            )
        except Exception:
            messagebox.showerror(
                "Error",
                "Please enter valid SAN value and loss format, such as 0, 1, 1d3, or 1d6."
            )

    # ======================
    # NPC Manager
    # ======================

    def show_npc_page(self):
        self.clear_content()
        self.selected_npc_index = None
        self.npc_entries = {}

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

        self.create_npc_input(basic_tab, "Name", 0)
        self.create_npc_input(basic_tab, "Age", 1)
        self.create_npc_input(basic_tab, "Gender", 2)
        self.create_npc_input(basic_tab, "Occupation", 3)
        self.create_npc_input(basic_tab, "Role", 4)
        self.create_npc_input(basic_tab, "Portrait", 5)

        tk.Button(
            basic_tab,
            text="Select Image",
            command=self.select_portrait
        ).grid(row=6, column=1, pady=10, sticky="w")

        attributes = ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU"]
        for i, attr in enumerate(attributes):
            self.create_npc_input(attr_tab, attr, i, default="50")

        status_fields = ["HP", "MP", "SAN", "Luck", "Move", "Build", "Damage Bonus"]
        for i, field in enumerate(status_fields):
            self.create_npc_input(combat_tab, field, i)

        combat_fields = ["Weapons", "Dodge", "Fighting"]
        for i, field in enumerate(combat_fields, start=len(status_fields)):
            self.create_npc_input(combat_tab, field, i)

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
            self.create_npc_input(skills_tab, skill, i)

        note_fields = [
            "Backstory",
            "Ideology",
            "Significant Person",
            "Treasured Possession",
            "Trait",
            "Note"
        ]

        for i, field in enumerate(note_fields):
            self.create_npc_input(notes_tab, field, i)

        button_frame = tk.Frame(left_frame, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save New NPC", command=self.handle_save_npc).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.handle_update_npc).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_npc_form).grid(row=0, column=2, padx=5)

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

    def create_npc_input(self, parent, label_text, row, default=""):
        tk.Label(parent, text=label_text, bg="#f5f5f5").grid(
            row=row, column=0, padx=8, pady=5, sticky="e"
        )

        entry = tk.Entry(parent, width=35)
        entry.grid(row=row, column=1, padx=8, pady=5)

        if default:
            entry.insert(0, default)

        self.npc_entries[label_text] = entry

    def select_portrait(self):
        file_path = filedialog.askopenfilename(
            title="Select NPC Portrait",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.npc_entries["Portrait"].delete(0, tk.END)
            self.npc_entries["Portrait"].insert(0, file_path)

    def get_npc_form_data(self):
        return {
            "basic_info": {
                "name": self.npc_entries["Name"].get(),
                "age": self.npc_entries["Age"].get(),
                "gender": self.npc_entries["Gender"].get(),
                "occupation": self.npc_entries["Occupation"].get(),
                "role": self.npc_entries["Role"].get(),
                "portrait": self.npc_entries["Portrait"].get()
            },
            "attributes": {
                "STR": self.npc_entries["STR"].get(),
                "CON": self.npc_entries["CON"].get(),
                "SIZ": self.npc_entries["SIZ"].get(),
                "DEX": self.npc_entries["DEX"].get(),
                "APP": self.npc_entries["APP"].get(),
                "INT": self.npc_entries["INT"].get(),
                "POW": self.npc_entries["POW"].get(),
                "EDU": self.npc_entries["EDU"].get()
            },
            "status": {
                "HP": self.npc_entries["HP"].get(),
                "MP": self.npc_entries["MP"].get(),
                "SAN": self.npc_entries["SAN"].get(),
                "Luck": self.npc_entries["Luck"].get(),
                "Move": self.npc_entries["Move"].get(),
                "Build": self.npc_entries["Build"].get(),
                "Damage Bonus": self.npc_entries["Damage Bonus"].get()
            },
            "combat": {
                "Weapons": self.npc_entries["Weapons"].get(),
                "Dodge": self.npc_entries["Dodge"].get(),
                "Fighting": self.npc_entries["Fighting"].get()
            },
            "skills": {
                "Spot Hidden": self.npc_entries["Spot Hidden"].get(),
                "Listen": self.npc_entries["Listen"].get(),
                "Psychology": self.npc_entries["Psychology"].get(),
                "Library Use": self.npc_entries["Library Use"].get(),
                "Stealth": self.npc_entries["Stealth"].get(),
                "Persuade": self.npc_entries["Persuade"].get(),
                "Fast Talk": self.npc_entries["Fast Talk"].get(),
                "Intimidate": self.npc_entries["Intimidate"].get(),
                "Medicine": self.npc_entries["Medicine"].get(),
                "Occult": self.npc_entries["Occult"].get()
            },
            "background": {
                "Backstory": self.npc_entries["Backstory"].get(),
                "Ideology": self.npc_entries["Ideology"].get(),
                "Significant Person": self.npc_entries["Significant Person"].get(),
                "Treasured Possession": self.npc_entries["Treasured Possession"].get(),
                "Trait": self.npc_entries["Trait"].get(),
                "Note": self.npc_entries["Note"].get()
            }
        }

    def clear_npc_form(self):
        for entry in self.npc_entries.values():
            entry.delete(0, tk.END)

        for key in ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU"]:
            self.npc_entries[key].insert(0, "50")

        self.selected_npc_index = None

    def fill_npc_form(self, npc):
        self.clear_npc_form()

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

            if field_name in self.npc_entries:
                self.npc_entries[field_name].delete(0, tk.END)
                self.npc_entries[field_name].insert(0, value)

    def handle_save_npc(self):
        data = self.get_npc_form_data()

        if not data["basic_info"]["name"]:
            messagebox.showerror("Error", "NPC name cannot be empty.")
            return

        create_npc(data)
        messagebox.showinfo("Success", "NPC saved successfully.")
        self.clear_npc_form()
        self.refresh_npc_list()

    def handle_update_npc(self):
        if self.selected_npc_index is None:
            messagebox.showerror("Error", "Please select an NPC first.")
            return

        data = self.get_npc_form_data()
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
        self.fill_npc_form(npcs[index])

    def handle_delete_npc(self):
        if self.selected_npc_index is None:
            messagebox.showerror("Error", "Please select an NPC first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this NPC?"
        )

        if confirm:
            success = delete_npc(self.selected_npc_index)

            if success:
                messagebox.showinfo("Success", "NPC deleted successfully.")
                self.selected_npc_index = None
                self.clear_npc_form()
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
        window.geometry("620x700")

        text_box = tk.Text(window, wrap="word", font=("Arial", 11))
        text_box.pack(fill="both", expand=True, padx=15, pady=15)

        text_box.insert("1.0", self.format_npc_detail(npc))
        text_box.config(state="disabled")

    def format_npc_detail(self, npc):
        text = ""

        for section_name, section_data in npc.items():
            text += f"=== {section_name} ===\n"
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    text += f"{key}: {value}\n"
            else:
                text += f"{section_data}\n"
            text += "\n"

        return text

    # ======================
    # Clue Manager
    # ======================

    def show_clues_page(self):
        self.clear_content()
        self.selected_clue_index = None
        self.clue_entries = {}
        self.displayed_clue_indices = []

        self.create_page_title("Clue Manager")

        main_frame = tk.Frame(self.content, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#f5f5f5")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        right_frame = tk.Frame(main_frame, bg="#f5f5f5")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.create_clue_input(left_frame, "Title", 0)
        self.create_clue_input(left_frame, "Location", 1)
        self.create_clue_input(left_frame, "Related NPC", 2)
        self.create_clue_input(left_frame, "Status", 3, default="Hidden")
        self.create_clue_input(left_frame, "Tags", 4)

        tk.Label(left_frame, text="Description", bg="#f5f5f5").grid(
            row=5, column=0, padx=8, pady=5, sticky="ne"
        )

        self.clue_description_text = tk.Text(left_frame, width=35, height=8)
        self.clue_description_text.grid(row=5, column=1, padx=8, pady=5)

        button_frame = tk.Frame(left_frame, bg="#f5f5f5")
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Save New Clue", command=self.handle_save_clue).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.handle_update_clue).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_clue_form).grid(row=0, column=2, padx=5)

        search_frame = tk.Frame(right_frame, bg="#f5f5f5")
        search_frame.pack(pady=5)

        self.clue_search_entry = tk.Entry(search_frame, width=30)
        self.clue_search_entry.grid(row=0, column=0, padx=5)

        tk.Button(search_frame, text="Search", command=self.handle_search_clue).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Show All", command=self.refresh_clue_list).grid(row=0, column=2, padx=5)

        tk.Label(
            right_frame,
            text="Clue List",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        ).pack(pady=5)

        self.clue_listbox = tk.Listbox(right_frame, height=22)
        self.clue_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(right_frame)
        scrollbar.pack(side="right", fill="y")

        self.clue_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.clue_listbox.yview)

        self.clue_listbox.bind("<<ListboxSelect>>", self.handle_select_clue)
        self.clue_listbox.bind("<Double-Button-1>", self.open_clue_detail_window)

        action_frame = tk.Frame(self.content, bg="#f5f5f5")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="View Detail", command=self.open_clue_detail_window).grid(row=0, column=0, padx=10)
        tk.Button(action_frame, text="Delete Selected Clue", command=self.handle_delete_clue).grid(row=0, column=1, padx=10)

        self.refresh_clue_list()

    def create_clue_input(self, parent, label_text, row, default=""):
        tk.Label(parent, text=label_text, bg="#f5f5f5").grid(
            row=row, column=0, padx=8, pady=5, sticky="e"
        )

        entry = tk.Entry(parent, width=35)
        entry.grid(row=row, column=1, padx=8, pady=5)

        if default:
            entry.insert(0, default)

        self.clue_entries[label_text] = entry

    def get_clue_form_data(self):
        return {
            "title": self.clue_entries["Title"].get(),
            "location": self.clue_entries["Location"].get(),
            "related_npc": self.clue_entries["Related NPC"].get(),
            "status": self.clue_entries["Status"].get(),
            "tags": self.clue_entries["Tags"].get(),
            "description": self.clue_description_text.get("1.0", tk.END).strip()
        }

    def clear_clue_form(self):
        for entry in self.clue_entries.values():
            entry.delete(0, tk.END)

        self.clue_entries["Status"].insert(0, "Hidden")
        self.clue_description_text.delete("1.0", tk.END)
        self.selected_clue_index = None

    def fill_clue_form(self, clue):
        self.clear_clue_form()

        self.clue_entries["Title"].insert(0, clue.get("title", ""))
        self.clue_entries["Location"].insert(0, clue.get("location", ""))
        self.clue_entries["Related NPC"].insert(0, clue.get("related_npc", ""))
        self.clue_entries["Status"].insert(0, clue.get("status", ""))
        self.clue_entries["Tags"].insert(0, clue.get("tags", ""))
        self.clue_description_text.insert("1.0", clue.get("description", ""))

    def handle_save_clue(self):
        data = self.get_clue_form_data()

        if not data["title"]:
            messagebox.showerror("Error", "Clue title cannot be empty.")
            return

        create_clue(data)
        messagebox.showinfo("Success", "Clue saved successfully.")
        self.clear_clue_form()
        self.refresh_clue_list()

    def handle_update_clue(self):
        if self.selected_clue_index is None:
            messagebox.showerror("Error", "Please select a clue first.")
            return

        data = self.get_clue_form_data()
        success = update_clue(self.selected_clue_index, data)

        if success:
            messagebox.showinfo("Success", "Clue updated successfully.")
            self.refresh_clue_list()
        else:
            messagebox.showerror("Error", "Update failed.")

    def refresh_clue_list(self):
        self.clue_listbox.delete(0, tk.END)
        self.displayed_clue_indices = []

        clues = get_all_clues()

        if not clues:
            self.clue_listbox.insert(tk.END, "No clue data.")
            return

        for index, clue in enumerate(clues):
            self.displayed_clue_indices.append(index)
            self.clue_listbox.insert(
                tk.END,
                f"{index + 1}. {clue.get('title', '')} | {clue.get('location', '')} | {clue.get('status', '')}"
            )

    def handle_select_clue(self, event=None):
        selected = self.clue_listbox.curselection()

        if not selected:
            return

        list_index = selected[0]

        if list_index >= len(self.displayed_clue_indices):
            return

        real_index = self.displayed_clue_indices[list_index]
        clues = get_all_clues()

        if real_index >= len(clues):
            return

        self.selected_clue_index = real_index
        self.fill_clue_form(clues[real_index])

    def handle_search_clue(self):
        keyword = self.clue_search_entry.get()

        self.clue_listbox.delete(0, tk.END)
        self.displayed_clue_indices = []

        results = search_clues(keyword)

        if not results:
            self.clue_listbox.insert(tk.END, "No matching clue found.")
            return

        for real_index, clue in results:
            self.displayed_clue_indices.append(real_index)
            self.clue_listbox.insert(
                tk.END,
                f"{real_index + 1}. {clue.get('title', '')} | {clue.get('location', '')} | {clue.get('status', '')}"
            )

    def handle_delete_clue(self):
        if self.selected_clue_index is None:
            messagebox.showerror("Error", "Please select a clue first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this clue?"
        )

        if confirm:
            success = delete_clue(self.selected_clue_index)

            if success:
                messagebox.showinfo("Success", "Clue deleted successfully.")
                self.selected_clue_index = None
                self.clear_clue_form()
                self.refresh_clue_list()
            else:
                messagebox.showerror("Error", "Delete failed.")

    def open_clue_detail_window(self, event=None):
        if self.selected_clue_index is None:
            messagebox.showerror("Error", "Please select a clue first.")
            return

        clues = get_all_clues()

        if self.selected_clue_index >= len(clues):
            return

        clue = clues[self.selected_clue_index]

        window = Toplevel(self.root)
        window.title(f"Clue Detail - {clue.get('title', '')}")
        window.geometry("500x500")

        detail_text = (
            f"Title: {clue.get('title', '')}\n"
            f"Location: {clue.get('location', '')}\n"
            f"Related NPC: {clue.get('related_npc', '')}\n"
            f"Status: {clue.get('status', '')}\n"
            f"Tags: {clue.get('tags', '')}\n\n"
            f"Description:\n{clue.get('description', '')}"
        )

        text_box = tk.Text(window, wrap="word", font=("Arial", 11))
        text_box.pack(fill="both", expand=True, padx=15, pady=15)
        text_box.insert("1.0", detail_text)
        text_box.config(state="disabled")

    # ======================
    # Campaign Manager
    # ======================

    def show_campaign_page(self):
        self.clear_content()
        self.selected_campaign_index = None
        self.campaign_entries = {}

        self.create_page_title("Campaign Manager")

        main_frame = tk.Frame(self.content, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#f5f5f5")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        right_frame = tk.Frame(main_frame, bg="#f5f5f5")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.create_campaign_input(left_frame, "Title", 0)
        self.create_campaign_input(left_frame, "System", 1, default="COC7")
        self.create_campaign_input(left_frame, "Keeper", 2)
        self.create_campaign_input(left_frame, "Status", 3, default="Planning")
        self.create_campaign_input(left_frame, "Tags", 4)

        tk.Label(left_frame, text="Description", bg="#f5f5f5").grid(
            row=5, column=0, padx=8, pady=5, sticky="ne"
        )

        self.campaign_description_text = tk.Text(left_frame, width=38, height=8)
        self.campaign_description_text.grid(row=5, column=1, padx=8, pady=5)

        tk.Label(left_frame, text="Notes", bg="#f5f5f5").grid(
            row=6, column=0, padx=8, pady=5, sticky="ne"
        )

        self.campaign_notes_text = tk.Text(left_frame, width=38, height=8)
        self.campaign_notes_text.grid(row=6, column=1, padx=8, pady=5)

        button_frame = tk.Frame(left_frame, bg="#f5f5f5")
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Save New Campaign", command=self.handle_save_campaign).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.handle_update_campaign).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_campaign_form).grid(row=0, column=2, padx=5)

        tk.Label(
            right_frame,
            text="Campaign List",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        ).pack(pady=5)

        self.campaign_listbox = tk.Listbox(right_frame, height=25)
        self.campaign_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(right_frame)
        scrollbar.pack(side="right", fill="y")

        self.campaign_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.campaign_listbox.yview)

        self.campaign_listbox.bind("<<ListboxSelect>>", self.handle_select_campaign)
        self.campaign_listbox.bind("<Double-Button-1>", self.open_campaign_detail_window)

        action_frame = tk.Frame(self.content, bg="#f5f5f5")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="View Detail", command=self.open_campaign_detail_window).grid(row=0, column=0, padx=10)
        tk.Button(action_frame, text="Delete Selected Campaign", command=self.handle_delete_campaign).grid(row=0, column=1, padx=10)

        self.refresh_campaign_list()

    def create_campaign_input(self, parent, label_text, row, default=""):
        tk.Label(parent, text=label_text, bg="#f5f5f5").grid(
            row=row, column=0, padx=8, pady=5, sticky="e"
        )

        entry = tk.Entry(parent, width=38)
        entry.grid(row=row, column=1, padx=8, pady=5)

        if default:
            entry.insert(0, default)

        self.campaign_entries[label_text] = entry

    def get_campaign_form_data(self):
        return {
            "title": self.campaign_entries["Title"].get(),
            "system": self.campaign_entries["System"].get(),
            "keeper": self.campaign_entries["Keeper"].get(),
            "status": self.campaign_entries["Status"].get(),
            "tags": self.campaign_entries["Tags"].get(),
            "description": self.campaign_description_text.get("1.0", tk.END).strip(),
            "notes": self.campaign_notes_text.get("1.0", tk.END).strip()
        }

    def clear_campaign_form(self):
        for entry in self.campaign_entries.values():
            entry.delete(0, tk.END)

        self.campaign_entries["System"].insert(0, "COC7")
        self.campaign_entries["Status"].insert(0, "Planning")
        self.campaign_description_text.delete("1.0", tk.END)
        self.campaign_notes_text.delete("1.0", tk.END)
        self.selected_campaign_index = None

    def fill_campaign_form(self, campaign):
        self.clear_campaign_form()

        self.campaign_entries["Title"].insert(0, campaign.get("title", ""))
        self.campaign_entries["System"].insert(0, campaign.get("system", ""))
        self.campaign_entries["Keeper"].insert(0, campaign.get("keeper", ""))
        self.campaign_entries["Status"].insert(0, campaign.get("status", ""))
        self.campaign_entries["Tags"].insert(0, campaign.get("tags", ""))
        self.campaign_description_text.insert("1.0", campaign.get("description", ""))
        self.campaign_notes_text.insert("1.0", campaign.get("notes", ""))

    def handle_save_campaign(self):
        data = self.get_campaign_form_data()

        if not data["title"]:
            messagebox.showerror("Error", "Campaign title cannot be empty.")
            return

        create_campaign(data)
        messagebox.showinfo("Success", "Campaign saved successfully.")
        self.clear_campaign_form()
        self.refresh_campaign_list()

    def handle_update_campaign(self):
        if self.selected_campaign_index is None:
            messagebox.showerror("Error", "Please select a campaign first.")
            return

        data = self.get_campaign_form_data()
        success = update_campaign(self.selected_campaign_index, data)

        if success:
            messagebox.showinfo("Success", "Campaign updated successfully.")
            self.refresh_campaign_list()
        else:
            messagebox.showerror("Error", "Update failed.")

    def refresh_campaign_list(self):
        self.campaign_listbox.delete(0, tk.END)

        campaigns = get_all_campaigns()

        if not campaigns:
            self.campaign_listbox.insert(tk.END, "No campaign data.")
            return

        for index, campaign in enumerate(campaigns, start=1):
            self.campaign_listbox.insert(
                tk.END,
                f"{index}. {campaign.get('title', '')} | {campaign.get('system', '')} | {campaign.get('status', '')}"
            )

    def handle_select_campaign(self, event=None):
        selected = self.campaign_listbox.curselection()

        if not selected:
            return

        index = selected[0]
        campaigns = get_all_campaigns()

        if index >= len(campaigns):
            return

        self.selected_campaign_index = index
        self.fill_campaign_form(campaigns[index])

    def handle_delete_campaign(self):
        if self.selected_campaign_index is None:
            messagebox.showerror("Error", "Please select a campaign first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this campaign?"
        )

        if confirm:
            success = delete_campaign(self.selected_campaign_index)

            if success:
                messagebox.showinfo("Success", "Campaign deleted successfully.")
                self.selected_campaign_index = None
                self.clear_campaign_form()
                self.refresh_campaign_list()
            else:
                messagebox.showerror("Error", "Delete failed.")

    def open_campaign_detail_window(self, event=None):
        if self.selected_campaign_index is None:
            messagebox.showerror("Error", "Please select a campaign first.")
            return

        campaigns = get_all_campaigns()

        if self.selected_campaign_index >= len(campaigns):
            return

        campaign = campaigns[self.selected_campaign_index]

        window = Toplevel(self.root)
        window.title(f"Campaign Detail - {campaign.get('title', '')}")
        window.geometry("550x520")

        detail_text = (
            f"Title: {campaign.get('title', '')}\n"
            f"System: {campaign.get('system', '')}\n"
            f"Keeper: {campaign.get('keeper', '')}\n"
            f"Status: {campaign.get('status', '')}\n"
            f"Tags: {campaign.get('tags', '')}\n\n"
            f"Description:\n{campaign.get('description', '')}\n\n"
            f"Notes:\n{campaign.get('notes', '')}"
        )

        text_box = tk.Text(window, wrap="word", font=("Arial", 11))
        text_box.pack(fill="both", expand=True, padx=15, pady=15)
        text_box.insert("1.0", detail_text)
        text_box.config(state="disabled")

    # ======================
    # Placeholder Pages
    # ======================

    def show_maps_page(self):
        self.show_placeholder_page("Maps", "Map tools will be added in a future version.")

    def show_timeline_page(self):
        self.show_placeholder_page("Timeline", "Timeline tools will be added in a future version.")

    def show_music_page(self):
        self.show_placeholder_page("Music", "Music control will be added in a future version.")

    def show_settings_page(self):
        self.show_placeholder_page("Settings", "Settings will be added in a future version.")

    def show_placeholder_page(self, title="Coming Soon", message="This feature will be added in a future version."):
        self.clear_content()
        self.create_page_title(title)

        tk.Label(
            self.content,
            text=message,
            font=("Arial", 14),
            bg="#f5f5f5"
        ).pack(pady=20)

    def run(self):
        self.root.mainloop()
