import tkinter as tk
from gui.intake_frame import IntakeFrame

def main():
    root = tk.Tk()
    root.title("Mapúa Findr - Intake System")
    root.geometry("520x640")
    root.resizable(False, False)

    intake_frame = IntakeFrame(root)
    intake_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()