import tkinter as tk
from tkinter import ttk
from gui.intake_frame import IntakeFrame
from gui.feed_frame import FeedFrame


class CodeOfConductView(ttk.Frame):
    def __init__(self, parent, on_agree_callback):
        super().__init__(parent, padding=24)
        self.parent = parent
        self.on_agree_callback = on_agree_callback

        self.parent.title("Mapúa Code of Conduct Confirmation")
        self.parent.geometry("500x260")

        header_lbl = ttk.Label(
            self,
            text="User Acknowledgment",
            font=("Segoe UI", 12, "bold")
        )
        header_lbl.pack(anchor="w", pady=(0, 10))

        statement_text = (
            "Under the Mapúa Code of Conduct, I acknowledge that all submitted "
            "and retrieved records must be truthful and made in good faith. "
            "Any fraudulent claims or tampering with reported items are subject "
            "to institutional disciplinary action."
        )
        statement_lbl = ttk.Label(
            self,
            text=statement_text,
            wraplength=450,
            justify="left"
        )
        statement_lbl.pack(anchor="w", pady=(0, 15))

        self.agreement_var = tk.BooleanVar(value=False)
        self.check_btn = ttk.Checkbutton(
            self,
            text="I understand and agree to adhere to the Mapúa Code of Conduct.",
            variable=self.agreement_var,
            command=self.toggle_button
        )
        self.check_btn.pack(anchor="w", pady=(0, 15))

        self.continue_btn = ttk.Button(
            self,
            text="Proceed to Mapúa Findr",
            state="disabled",
            command=self.proceed
        )
        self.continue_btn.pack(anchor="e")

    def toggle_button(self):
        if self.agreement_var.get():
            self.continue_btn.config(state="normal")
        else:
            self.continue_btn.config(state="disabled")

    def proceed(self):
        self.destroy()
        self.on_agree_callback()


def start_main_system(root):
    root.title("Mapúa Findr")
    root.geometry("620x720")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Tab 1: Feed Frame (Browse items)
    feed_tab = FeedFrame(notebook)
    notebook.add(feed_tab, text=" Browse Feed ")

    # Tab 2: Intake Frame (Log items)
    intake_tab = IntakeFrame(notebook)
    notebook.add(intake_tab, text=" Report Item ")

    # Refresh feed automatically whenever the user clicks the "Browse Feed" tab
    def on_tab_selected(event):
        selected_widget = root.nametowidget(notebook.select())
        if selected_widget == feed_tab:
            feed_tab.load_feed()

    notebook.bind("<<NotebookTabChanged>>", on_tab_selected)


def main():
    root = tk.Tk()
    root.resizable(False, False)

    coc_view = CodeOfConductView(root, lambda: start_main_system(root))
    coc_view.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()