from distutils.log import error
import tkinter as tk
from tkinter.font import BOLD
import file_operations as fo
from tkinter import END, filedialog
import os

replay_directory = os.path.expandvars("%LOCALAPPDATA%\\RivalsOfAether\\replays")

def run_gui():
    window = tk.Tk()
    configure_window(window)
    setup_grid(window)

    window.mainloop()

def configure_window(window):
    window.title("Rivals Replay Tool")
    window.geometry("640x230")
    window.configure(background="grey")
    window.resizable(False, False)

    for i in range(4):
        window.rowconfigure(i, weight=0)

    window.columnconfigure(0, minsize=150, weight=1)
    window.columnconfigure(1, minsize=75, weight=1)
    window.columnconfigure(2, minsize=150, weight=1)
    window.columnconfigure(3, minsize=75, weight=1)

def setup_grid(window):
    setup_replay_folder_controls(window)
    setup_target_folder_controls(window)
    setup_file_count_controls(window)
    setup_set_name_controls(window)
    setup_error_label(window)
    setup_submit_button(window)    

def setup_replay_folder_controls(window):
    replay_folder_label = tk.Label(window, text="Folder Containing Replays:", bg="grey", font=("Arial", 13))
    replay_folder_label.grid(row=0, column=0, sticky="sw", padx=5, pady=5)

    replay_folder_text = tk.Entry(window, font=("Arial", 13))
    replay_folder_text.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    replay_folder_text.insert(0, replay_directory)
    replay_folder_text.config(state="readonly")
    
    replay_file_button = tk.Button(window, padx=10, text="Select Folder", command=lambda: add_file(replay_folder_text))
    replay_file_button.grid(row=1, column=1, sticky="w", pady=5)

def setup_target_folder_controls(window):
    target_folder_label = tk.Label(window, text="Target Folder For Zip File:", bg="grey", font=("Arial", 13))
    target_folder_label.grid(row=0, column=2, sticky="sw", padx=5, pady=5)

    target_folder_text = tk.Entry(window, font=("Arial", 13), state="readonly")
    target_folder_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

    target_file_button = tk.Button(window, padx=10, text="Select Folder", command=lambda: add_file(target_folder_text))
    target_file_button.grid(row=1, column=3, sticky="w", pady=5)

    config = fo.load()
    if (config is not None and "targetDirectory" in config):
        target_folder_text.config(state="normal")
        target_folder_text.insert(0, config["targetDirectory"])
        target_folder_text.config(state="readonly")

def setup_file_count_controls(window):
    file_count_label = tk.Label(window, text="Number of Files:", bg="grey", font=("Arial", 13))
    file_count_label.grid(row=2, column=0, sticky="sw", padx=5, pady=5)

    file_count_text = tk.Entry(window, font=("Arial", 13))
    file_count_text.grid(row=3, column=0, sticky="w", padx=5, pady=5)

    suggested_file_count = fo.parse_suggested_game_count(replay_directory)
    file_count_text.insert(0, suggested_file_count)

def setup_set_name_controls(window):
    set_name_label = tk.Label(window, text="Set Name:", bg="grey", font=("Arial", 13))
    set_name_label.grid(row=2, column=2, sticky="sw", padx=5, pady=5)

    set_name_text = tk.Entry(window, font=("Arial", 13))
    set_name_text.grid(row=3, column=2, sticky="w", padx=5, pady=5)

    suggested_set_name = fo.parse_suggested_set_name(replay_directory)
    set_name_text.insert(0, suggested_set_name)

def setup_error_label(window):
    error_label = tk.Label(window, bg="grey", font=("Arial", 15))
    error_label.grid(row=4, column=0, columnspan=4)

def setup_submit_button(window):
    blank_label = tk.Label(window, bg="grey")
    blank_label.grid(row=4, column=0, sticky="sw", padx=5, pady=5)

    submit_button = tk.Button(window, font=("Arial", 14, BOLD), text="Zip It!", command=lambda: copy_and_zip_files(window))
    submit_button.grid(row=5, column=0, columnspan=4)

def add_file(folder_text):
    file_name = filedialog.askdirectory(initialdir="/", title="Select Replay Folder")
    folder_text.config(state="normal")
    folder_text.delete(0, END)
    folder_text.insert(0, file_name)
    folder_text.config(state="readonly")

def copy_and_zip_files(window):
    error_label = window.children["!label5"]
    error_label.config(text="")
    replay_folder = window.children["!entry"].get()
    target_folder = window.children["!entry2"].get()
    file_count_text = window.children["!entry3"].get()
    set_name = window.children["!entry4"].get()
    
    try:
        if (not file_count_text.isdigit()):
            raise TypeError("Value for number of files is not a number")

        fo.copy_most_recent_files(replay_folder, target_folder, int(file_count_text), set_name)
        fo.zip_and_delete_set(target_folder + "\\" + set_name)
        fo.save({'targetDirectory': target_folder})
        error_label.config(fg="spring green")
        error_label.config(text="Done!")
    except Exception as e:
        print("caught")
        error_label.config(fg="red")
        error_label.config(text=str(e))
