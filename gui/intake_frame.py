import os
import shutil
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from models.entities import insert_item

class IntakeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        self.parent = parent
        self.selected_image_path = None
        self.preview_photo = None
        self._build_ui()

    def select_photo(self):
        file_types = [("Image files", "*.png;*.jpg;*.jpeg;*.webp")]
        file_path = filedialog.askopenfilename(title="Select Item Photo", filetypes=file_types)
        
        if file_path:
            self.selected_image_path = file_path
            
            # Load and resize thumbnail preview
            img = Image.open(file_path)
            img.thumbnail((80, 80))
            self.preview_photo = ImageTk.PhotoImage(img)
            
            self.preview_label.config(image=self.preview_photo, text="")

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

        # Photo upload
        ttk.Label(self, text="Item Photo:").grid(row=10, column=0, sticky="w", pady=6)

        photo_frame = ttk.Frame(self)
        photo_frame.grid(row=10, column=1, sticky="w", pady=6)

        self.upload_btn = ttk.Button(photo_frame, text="Choose Image...", command=self.select_photo)
        self.upload_btn.pack(side="left", padx=(0, 10))

        self.preview_label = tk.Label(photo_frame, text="No image selected", bg="#e0e0e0", width=18, height=4)
        self.preview_label.pack(side="left")

        # Submit Button
        submit_btn = ttk.Button(self, text="Submit Item", command=self._handle_submit)
        submit_btn.grid(row=11, column=0, columnspan=2, pady=(15, 0))

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
        # Handle Photo Saving
        image_db_path = None
        if self.selected_image_path:
            import time
            upload_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            
            ext = os.path.splitext(self.selected_image_path)[1]
            dest_filename = f"item_{int(time.time())}{ext}"
            dest_path = os.path.join(upload_dir, dest_filename)
            shutil.copy(self.selected_image_path, dest_path)
            
            image_db_path = os.path.join("uploads", dest_filename)

        success, message = insert_item(
            title=title,
            category=category,
            public_description=public_desc,
            campus=campus,
            building=building,
            room=room,
            storage_bin=storage_bin,
            hidden_specifications=hidden_specs,
            date_found=date_found,
            image_path=image_db_path
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
        self.selected_image_path = None
        self.preview_label.config(image="", text="No image selected")