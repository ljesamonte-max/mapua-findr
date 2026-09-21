import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models.entities import insert_item

class IntakeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Label(self, text="Log Found Item", font=("Helvetica", 16, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Title
        ttk.Label(self, text="Item Title:*").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_title = ttk.Entry(self, width=40)
        self.entry_title.grid(row=1, column=1, sticky="ew", pady=4)

        # Category
        ttk.Label(self, text="Category:*").grid(row=2, column=0, sticky="w", pady=4)
        self.combo_category = ttk.Combobox(
            self,
            values=["Electronics", "Cards / IDs", "Tumbler", "Umbrella", "Apparel", "Keys", "Other"],
            state="readonly",
            width=38
        )
        self.combo_category.current(0)
        self.combo_category.grid(row=2, column=1, sticky="ew", pady=4)

        # Campus
        ttk.Label(self, text="Campus:*").grid(row=3, column=0, sticky="w", pady=4)
        self.combo_campus = ttk.Combobox(
            self,
            values=["Intramuros", "Makati"],
            state="readonly",
            width=38
        )
        self.combo_campus.current(0)
        self.combo_campus.grid(row=3, column=1, sticky="ew", pady=4)

        # Building
        ttk.Label(self, text="Building:*").grid(row=4, column=0, sticky="w", pady=4)
        self.entry_building = ttk.Entry(self, width=40)
        self.entry_building.grid(row=4, column=1, sticky="ew", pady=4)

        # Room (Optional)
        ttk.Label(self, text="Room (Optional):").grid(row=5, column=0, sticky="w", pady=4)
        self.entry_room = ttk.Entry(self, width=40)
        self.entry_room.grid(row=5, column=1, sticky="ew", pady=4)

        # Storage Bin
        ttk.Label(self, text="Storage Bin:*").grid(row=6, column=0, sticky="w", pady=4)
        self.entry_bin = ttk.Entry(self, width=40)
        self.entry_bin.grid(row=6, column=1, sticky="ew", pady=4)

        # Date Found (YYYY-MM-DD)
        ttk.Label(self, text="Date Found (YYYY-MM-DD):*").grid(row=7, column=0, sticky="w", pady=4)
        self.entry_date = ttk.Entry(self, width=40)
        self.entry_date.insert(0, str(date.today()))
        self.entry_date.grid(row=7, column=1, sticky="ew", pady=4)

        # Public Description
        ttk.Label(self, text="Public Description:*").grid(row=8, column=0, sticky="nw", pady=4)
        self.text_public = tk.Text(self, width=40, height=3, font=("Helvetica", 9))
        self.text_public.grid(row=8, column=1, sticky="ew", pady=4)

        # Hidden Specifications (Verification Details)
        ttk.Label(self, text="Hidden Specs (Private):*").grid(row=9, column=0, sticky="nw", pady=4)
        self.text_hidden = tk.Text(self, width=40, height=3, font=("Helvetica", 9))
        self.text_hidden.grid(row=9, column=1, sticky="ew", pady=4)

        # Submit Button
        submit_btn = ttk.Button(self, text="Submit Item", command=self._handle_submit)
        submit_btn.grid(row=10, column=0, columnspan=2, pady=(15, 0))

    def _handle_submit(self):
        title = self.entry_title.get()
        category = self.combo_category.get()
        campus = self.combo_campus.get()
        building = self.entry_building.get()
        room = self.entry_room.get()
        storage_bin = self.entry_bin.get()
        date_found = self.entry_date.get()
        public_desc = self.text_public.get("1.0", tk.END)
        hidden_specs = self.text_hidden.get("1.0", tk.END)

        # Validate mandatory fields
        if not all([title.strip(), category.strip(), campus.strip(), building.strip(),
                    storage_bin.strip(), date_found.strip(), public_desc.strip(), hidden_specs.strip()]):
            messagebox.showwarning("Validation Error", "Please fill in all required (*) fields.")
            return

        # Insert to MySQL
        success, message = insert_item(
            title=title,
            category=category,
            public_description=public_desc,
            campus=campus,
            building=building,
            room=room,
            storage_bin=storage_bin,
            hidden_specifications=hidden_specs,
            date_found=date_found
        )

        if success:
            messagebox.showinfo("Success", message)
            self._clear_form()
        else:
            messagebox.showerror("Error", message)

    def _clear_form(self):
        self.entry_title.delete(0, tk.END)
        self.entry_building.delete(0, tk.END)
        self.entry_room.delete(0, tk.END)
        self.entry_bin.delete(0, tk.END)
        self.text_public.delete("1.0", tk.END)
        self.text_hidden.delete("1.0", tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, str(date.today()))