import glob
import os
import shutil

def copy_most_recent_files(replay_folder, target_folder, number_of_files):
    if (not os.path.isdir(replay_folder)):
        raise FileNotFoundError("Could not find replays folder")
    if (not os.path.isdir(target_folder)):
        raise FileNotFoundError("Could not find destination folder")
    
    list_of_files = glob.glob(replay_folder + "/*")
    if (len(list_of_files) < number_of_files):
        raise FileNotFoundError("Could not find replays ")
    sorted_files = sorted(list_of_files, key=os.path.getmtime)
    
    for i in range(number_of_files):
        file_name = sorted_files[i].split('\\')[-1]
        shutil.copyfile(sorted_files[i], target_folder + "\\" + file_name)
