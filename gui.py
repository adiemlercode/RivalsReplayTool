from cgitb import text
from msilib.schema import Font
from sys import maxsize
import tkinter as tk
from tkinter.font import BOLD, ITALIC
import file_operations as fo
from tkinter import CENTER, DISABLED, INSERT, filedialog, Text

def create_gui():
    window = tk.Tk()
    window.title("Rivals Replay Tool")
    window.geometry("650x500")
    window.configure(background="grey")

    for i in range(4):
        window.rowconfigure(i, weight=0)

    window.columnconfigure(0, minsize=150, weight=1)
    window.columnconfigure(1, minsize=75, weight=1)
    window.columnconfigure(2, minsize=150, weight=1)
    window.columnconfigure(3, minsize=75, weight=1)

    replay_folder_label = tk.Label(window, text="Folder Containing Replays:", bg="grey", font=("Arial", 13))
    replay_folder_label.grid(row=0, column=0, sticky="sw", padx=5, pady=5)

    target_folder_label = tk.Label(window, text="Target Folder For Zip File:", bg="grey", font=("Arial", 13))
    target_folder_label.grid(row=0, column=2, sticky="sw", padx=5, pady=5)

    replay_folder_text = tk.Entry(window, font=("Arial", 14), state=DISABLED)
    replay_folder_text.grid(row=1, column=0, sticky="w", padx=5, pady=5)

    replay_file_button = tk.Button(window, padx=10, text="Select Folder")
    replay_file_button.grid(row=1, column=1, sticky="w", pady=5)

    target_folder_text = tk.Entry(window, font=("Arial", 14), state=DISABLED)
    target_folder_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

    target_file_button = tk.Button(window, padx=10, text="Select Folder")
    target_file_button.grid(row=1, column=3, sticky="w", pady=5)

    file_count_label = tk.Label(window, text="Number of Files:", bg="grey", font=("Arial", 13))
    file_count_label.grid(row=2, column=0, sticky="sw", padx=5, pady=5)

    set_name_label = tk.Label(window, text="Set Name:", bg="grey", font=("Arial", 13))
    set_name_label.grid(row=2, column=2, sticky="sw", padx=5, pady=5)

    file_count_text = tk.Entry(window, font=("Arial", 14))
    file_count_text.grid(row=3, column=0, sticky="w", padx=5, pady=5)

    set_name_text = tk.Entry(window, font=("Arial", 14))
    set_name_text.grid(row=3, column=2, sticky="w", padx=5, pady=5)

    blank_label = tk.Label(window, bg="grey")
    blank_label.grid(row=4, column=0, sticky="sw", padx=5, pady=5)

    submit_button = tk.Button(window, font=("Arial", 14, BOLD), text="Zip It!")
    submit_button.grid(row=5, column=0, sticky="sw", padx=5, pady=5)

    window.mainloop()
