import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database.db_connection import get_connection


class FeedFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=16)
        self.parent = parent
        self.image_cache = []  # Keep references so Python doesn't garbage collect images

        # Header Title
        title_lbl = ttk.Label(self, text="Lost & Found Feed", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(anchor="w", pady=(0, 10))

        # Search and Filter Toolbar
        filter_box = ttk.Frame(self)
        filter_box.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_box, text="Search:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_box, textvariable=self.search_var, width=25)
        self.search_entry.pack(side="left", padx=(0, 10))

        search_btn = ttk.Button(filter_box, text="Search", command=self.load_feed)
        search_btn.pack(side="left", padx=(0, 5))

        refresh_btn = ttk.Button(filter_box, text="Reset", command=self.reset_feed)
        refresh_btn.pack(side="left")

        # Scrollable Canvas Setup
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Keep frame width aligned with canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.load_feed()

    def reset_feed(self):
        self.search_var.set("")
        self.load_feed()

    def load_feed(self):
        # Clear existing entries
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_cache.clear()

        query_term = self.search_var.get().strip()

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            if query_term:
                query = """
                    SELECT * FROM items 
                    WHERE title LIKE %s OR category LIKE %s OR building LIKE %s
                    ORDER BY created_at DESC
                """
                like_pattern = f"%{query_term}%"
                cursor.execute(query, (like_pattern, like_pattern, like_pattern))
            else:
                cursor.execute("SELECT * FROM items ORDER BY created_at DESC")

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if not rows:
                ttk.Label(
                    self.scrollable_frame, 
                    text="No reported items match your criteria.", 
                    font=("Segoe UI", 10, "italic")
                ).pack(pady=20)
                return

            for item in rows:
                self.create_item_card(item)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch records:\n{e}")

    def create_item_card(self, item):
        card = ttk.LabelFrame(
            self.scrollable_frame,
            text=f" [{item.get('status', 'Surrendered')}] {item.get('title', 'Unknown Item')} ",
            padding=10
        )
        card.pack(fill="x", expand=True, pady=6, padx=4)

        body = ttk.Frame(card)
        body.pack(fill="x", expand=True)

        # Image thumbnail column
        img_lbl = ttk.Label(body)
        img_lbl.pack(side="left", padx=(0, 12), anchor="n")

        image_path = item.get("image_path")
        if image_path and os.path.exists(image_path):
            try:
                pil_img = Image.open(image_path)
                pil_img.thumbnail((90, 90))
                tk_img = ImageTk.PhotoImage(pil_img)
                self.image_cache.append(tk_img)
                img_lbl.configure(image=tk_img)
            except Exception:
                img_lbl.configure(text="[Image Error]")
        else:
            img_lbl.configure(text="[No Image]")

        # Details column
        info_col = ttk.Frame(body)
        info_col.pack(side="left", fill="both", expand=True)

        meta_text = (
            f"Category: {item.get('category')}  |  "
            f"Campus: {item.get('campus')}  |  "
            f"Location: {item.get('building')} ({item.get('room') or 'N/A'})\n"
            f"Date Found: {item.get('date_found')}"
        )
        ttk.Label(info_col, text=meta_text, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))

        desc_text = item.get("public_description") or "No description provided."
        ttk.Label(info_col, text=desc_text, wraplength=320, justify="left").pack(anchor="w")