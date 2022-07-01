from datetime import date, datetime
import glob
import os
import shutil


def copy_most_recent_files(replay_folder, target_folder, number_of_files, set_name):
    # verify folders exist
    if (not os.path.isdir(replay_folder)):
        raise FileNotFoundError("Could not find replays folder")
    if (not os.path.isdir(target_folder)):
        raise FileNotFoundError("Could not find destination folder")

    # get replays and sort by recency
    list_of_files = glob.glob(replay_folder + "/*")
    if (len(list_of_files) < number_of_files):
        raise FileNotFoundError("Could not find replays ")
    sorted_files = sorted(list_of_files, key=os.path.getmtime)

    # make set directory
    if (os.path.isdir(target_folder + "\\" + set_name)):
        set_name = set_name + str(date.today())
    os.mkdir(target_folder + "\\" + set_name)
    
    #copy files over to set directory
    for i in range(number_of_files):
        file_name = sorted_files[i].split('\\')[-1]
        shutil.copyfile(sorted_files[i], target_folder + "\\" + set_name + "\\" + file_name)

def zip_and_delete_set(set_folder):
    shutil.make_archive(set_folder, "zip", set_folder)
    shutil.rmtree(set_folder)
