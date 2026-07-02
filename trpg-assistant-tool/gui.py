import tkinter as tk
from tkinter import messagebox

from dice import roll_dice
from npc import add_npc, get_all_npcs, search_npcs, delete_npc


class TRPGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRPG Keeper Studio")
        self.root.geometry("900x600")

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
    self.create_sidebar_button("📖 Clues", self.show_clues_page)
    self.create_sidebar_button("🗺 Maps", self.show_maps_page)
    self.create_sidebar_button("📅 Timeline", self.show_timeline_page)
    self.create_sidebar_button("🎵 Music", self.show_music_page)
    self.create_sidebar_button("📁 Campaign Manager", self.show_campaign_page)
    self.create_sidebar_button("⚙ Settings", self.show_settings_page)

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
        title.pack(pady=20)

    def show_dice_page(self):
        self.clear_content()
        self.create_page_title("Dice Roller")

        form_frame = tk.Frame(self.content, bg="#f5f5f5")
        form_frame.pack(pady=20)

        dice_label = tk.Label(
            form_frame,
            text="Dice Format:",
            bg="#f5f5f5"
        )
        dice_label.grid(row=0, column=0, padx=10, pady=10)

        self.dice_entry = tk.Entry(form_frame, width=30)
        self.dice_entry.grid(row=0, column=1, padx=10, pady=10)
        self.dice_entry.insert(0, "1d100")

        roll_button = tk.Button(
            form_frame,
            text="Roll Dice",
            command=self.handle_roll_dice
        )
        roll_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.dice_result = tk.Label(
            self.content,
            text="Result will appear here.",
            font=("Arial", 14),
            bg="#f5f5f5"
        )
        self.dice_result.pack(pady=20)

    def handle_roll_dice(self):
        try:
            dice_text = self.dice_entry.get()
            results, total = roll_dice(dice_text)
            self.dice_result.config(text=f"Results: {results}\nTotal: {total}")
        except:
            messagebox.showerror(
                "Error",
                "Please enter dice format like 1d100 or 2d6."
            )

    def show_npc_page(self):
        self.clear_content()
        self.create_page_title("NPC Manager")

        form_frame = tk.Frame(self.content, bg="#f5f5f5")
        form_frame.pack(pady=10)

        self.name_entry = self.create_form_input(form_frame, "Name", 0)
        self.age_entry = self.create_form_input(form_frame, "Age", 1)
        self.occupation_entry = self.create_form_input(form_frame, "Occupation", 2)
        self.role_entry = self.create_form_input(form_frame, "Role", 3)
        self.note_entry = self.create_form_input(form_frame, "Note", 4)

        save_button = tk.Button(
            form_frame,
            text="Save NPC",
            command=self.handle_save_npc
        )
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

        search_frame = tk.Frame(self.content, bg="#f5f5f5")
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=0, padx=5)

        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.handle_search_npc
        )
        search_button.grid(row=0, column=1, padx=5)

        show_all_button = tk.Button(
            search_frame,
            text="Show All",
            command=self.refresh_npc_list
        )
        show_all_button.grid(row=0, column=2, padx=5)

        list_frame = tk.Frame(self.content, bg="#f5f5f5")
        list_frame.pack(fill="both", expand=True, padx=40, pady=10)

        self.npc_listbox = tk.Listbox(list_frame, height=10)
        self.npc_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.npc_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.npc_listbox.yview)

        delete_button = tk.Button(
            self.content,
            text="Delete Selected NPC",
            command=self.handle_delete_npc
        )
        delete_button.pack(pady=10)

        self.refresh_npc_list()

    def create_form_input(self, parent, label_text, row):
        label = tk.Label(parent, text=label_text, bg="#f5f5f5")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

        entry = tk.Entry(parent, width=40)
        entry.grid(row=row, column=1, padx=10, pady=5)

        return entry

    def handle_save_npc(self):
        name = self.name_entry.get()

        if not name:
            messagebox.showerror("Error", "NPC name cannot be empty.")
            return

        add_npc(
            name,
            self.age_entry.get(),
            self.occupation_entry.get(),
            self.role_entry.get(),
            self.note_entry.get()
        )

        messagebox.showinfo("Success", "NPC saved successfully.")
        self.show_npc_page()

    def refresh_npc_list(self):
        self.npc_listbox.delete(0, tk.END)

        npcs = get_all_npcs()

        if not npcs:
            self.npc_listbox.insert(tk.END, "No NPC data.")
            return

        for index, npc in enumerate(npcs, start=1):
            text = f"{index}. {npc['name']} | {npc['occupation']} | {npc['role']}"
            self.npc_listbox.insert(tk.END, text)

    def handle_search_npc(self):
        keyword = self.search_entry.get()

        self.npc_listbox.delete(0, tk.END)

        results = search_npcs(keyword)

        if not results:
            self.npc_listbox.insert(tk.END, "No matching NPC found.")
            return

        for npc in results:
            text = f"{npc['name']} | {npc['occupation']} | {npc['role']}"
            self.npc_listbox.insert(tk.END, text)

    def handle_delete_npc(self):
        selected = self.npc_listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Please select an NPC to delete.")
            return

        index = selected[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this NPC?"
        )

        if confirm:
            success = delete_npc(index)

            if success:
                messagebox.showinfo("Success", "NPC deleted successfully.")
                self.refresh_npc_list()
            else:
                messagebox.showerror("Error", "Delete failed.")

    def show_placeholder_page(self):
        self.clear_content()
        self.create_page_title("Coming Soon")
        label = tk.Label(
            self.content,
            text="This feature will be added in a future version.",
            font=("Arial", 14),
            bg="#f5f5f5"
        )
        label.pack(pady=20)
def show_clues_page(self):
    self.clear_content()
    self.create_page_title("Clues")
    label = tk.Label(
        self.content,
        text="Clue management will be added here.\n\nFuture features:\n- Add clue\n- View clues\n- Link clues to NPCs\n- Mark clue as discovered",
        font=("Arial", 14),
        bg="#f5f5f5"
    )
    label.pack(pady=20)


def show_maps_page(self):
    self.clear_content()
    self.create_page_title("Maps")
    label = tk.Label(
        self.content,
        text="Map tools will be added here.\n\nFuture features:\n- Add map image\n- View maps\n- Add location notes",
        font=("Arial", 14),
        bg="#f5f5f5"
    )
    label.pack(pady=20)


def show_timeline_page(self):
    self.clear_content()
    self.create_page_title("Timeline")
    label = tk.Label(
        self.content,
        text="Timeline system will be added here.\n\nFuture features:\n- Add event\n- View story timeline\n- Sort events by time",
        font=("Arial", 14),
        bg="#f5f5f5"
    )
    label.pack(pady=20)


def show_music_page(self):
    self.clear_content()
    self.create_page_title("Music")
    label = tk.Label(
        self.content,
        text="Music control will be added here.\n\nFuture features:\n- Add music file\n- Play background music\n- Stop music",
        font=("Arial", 14),
        bg="#f5f5f5"
    )
    label.pack(pady=20)


def show_campaign_page(self):
    self.clear_content()
    self.create_page_title("Campaign Manager")
    label = tk.Label(
        self.content,
        text="Campaign management will be added here.\n\nFuture features:\n- Create campaign\n- Save campaign notes\n- Manage NPCs, clues, maps and timeline by campaign",
        font=("Arial", 14),
        bg="#f5f5f5"
    )
    label.pack(pady=20)


def show_settings_page(self):
    self.clear_content()
    self.create_page_title("Settings")
    label = tk.Label(
        self.content,
        text="Settings will be added here.\n\nFuture features:\n- Theme settings\n- Data path settings\n- Export and import options",
        font=("Arial", 14),
        bg="#f5f5f5"
    )
    label.pack(pady=20)
    def run(self):
        self.root.mainloop()
