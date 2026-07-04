import tkinter as tk
from tkinter import messagebox, Toplevel

from dice import roll_dice
from npc import add_npc, get_all_npcs, update_npc, delete_npc


class TRPGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRPG Keeper Studio")
        self.root.geometry("950x620")

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
        title.pack(pady=20)

    def show_dice_page(self):
        self.clear_content()
        self.create_page_title("CoC Dice Roller")

        form_frame = tk.Frame(self.content, bg="#f5f5f5")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Dice Format:", bg="#f5f5f5").grid(
            row=0, column=0, padx=10, pady=10
        )

        self.dice_entry = tk.Entry(form_frame, width=30)
        self.dice_entry.grid(row=0, column=1, padx=10, pady=10)
        self.dice_entry.insert(0, "1d100")

        tk.Button(
            form_frame,
            text="Roll Dice",
            command=self.handle_roll_dice
        ).grid(row=1, column=0, columnspan=2, pady=10)

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
        self.create_page_title("NPC Manager")

        main_frame = tk.Frame(self.content, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(side="left", fill="y", padx=20)

        self.name_entry = self.create_form_input(form_frame, "Name", 0)
        self.age_entry = self.create_form_input(form_frame, "Age", 1)
        self.occupation_entry = self.create_form_input(form_frame, "Occupation", 2)
        self.role_entry = self.create_form_input(form_frame, "Role", 3)
        self.note_entry = self.create_form_input(form_frame, "Note", 4)
        self.portrait_entry = self.create_form_input(form_frame, "Portrait Path", 5)

        tk.Button(
            form_frame,
            text="Save New NPC",
            command=self.handle_save_npc
        ).grid(row=6, column=0, columnspan=2, pady=8)

        tk.Button(
            form_frame,
            text="Update Selected NPC",
            command=self.handle_update_npc
        ).grid(row=7, column=0, columnspan=2, pady=8)

        list_frame = tk.Frame(main_frame, bg="#f5f5f5")
        list_frame.pack(side="right", fill="both", expand=True, padx=20)

        tk.Label(
            list_frame,
            text="NPC List",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        ).pack(pady=5)

        self.npc_listbox = tk.Listbox(list_frame, height=18)
        self.npc_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.npc_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.npc_listbox.yview)

        self.npc_listbox.bind("<<ListboxSelect>>", self.handle_select_npc)
        self.npc_listbox.bind("<Double-Button-1>", self.open_npc_detail_window)

        button_frame = tk.Frame(self.content, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="View Detail",
            command=self.open_npc_detail_window
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Delete Selected NPC",
            command=self.handle_delete_npc
        ).grid(row=0, column=1, padx=10)

        self.refresh_npc_list()

    def create_form_input(self, parent, label_text, row):
        tk.Label(parent, text=label_text, bg="#f5f5f5").grid(
            row=row, column=0, padx=10, pady=5, sticky="e"
        )

        entry = tk.Entry(parent, width=35)
        entry.grid(row=row, column=1, padx=10, pady=5)

        return entry

    def clear_form(self):
        for entry in [
            self.name_entry,
            self.age_entry,
            self.occupation_entry,
            self.role_entry,
            self.note_entry,
            self.portrait_entry
        ]:
            entry.delete(0, tk.END)

    def fill_form(self, npc):
        self.clear_form()
        self.name_entry.insert(0, npc.get("name", ""))
        self.age_entry.insert(0, npc.get("age", ""))
        self.occupation_entry.insert(0, npc.get("occupation", ""))
        self.role_entry.insert(0, npc.get("role", ""))
        self.note_entry.insert(0, npc.get("note", ""))
        self.portrait_entry.insert(0, npc.get("portrait", ""))

    def handle_save_npc(self):
        name = self.name_entry.get()

        if not name:
            messagebox.showerror("Error", "NPC name cannot be empty.")
            return

        add_npc(
            self.name_entry.get(),
            self.age_entry.get(),
            self.occupation_entry.get(),
            self.role_entry.get(),
            self.note_entry.get(),
            self.portrait_entry.get()
        )

        messagebox.showinfo("Success", "NPC saved successfully.")
        self.clear_form()
        self.refresh_npc_list()

    def handle_update_npc(self):
        if self.selected_npc_index is None:
            messagebox.showerror("Error", "Please select an NPC first.")
            return

        success = update_npc(
            self.selected_npc_index,
            self.name_entry.get(),
            self.age_entry.get(),
            self.occupation_entry.get(),
            self.role_entry.get(),
            self.note_entry.get(),
            self.portrait_entry.get()
        )

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
            text = f"{index}. {npc.get('name', '')} | {npc.get('occupation', '')} | {npc.get('role', '')}"
            self.npc_listbox.insert(tk.END, text)

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

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this NPC?"
        )

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
        window.title(f"NPC Detail - {npc.get('name', '')}")
        window.geometry("400x420")

        detail_text = (
            f"Name: {npc.get('name', '')}\n"
            f"Age: {npc.get('age', '')}\n"
            f"Occupation: {npc.get('occupation', '')}\n"
            f"Role: {npc.get('role', '')}\n"
            f"Portrait: {npc.get('portrait', '')}\n\n"
            f"Note:\n{npc.get('note', '')}"
        )

        tk.Label(
            window,
            text=detail_text,
            justify="left",
            font=("Arial", 12),
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
