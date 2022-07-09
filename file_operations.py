from datetime import date
import glob
import os
import pickle
import re
import shutil


def copy_most_recent_files(replay_folder, target_folder, number_of_files, set_name):
    # verify folders exist
    if (not os.path.isdir(replay_folder)):
        raise FileNotFoundError("Could not find replays folder")
    if (not os.path.isdir(target_folder)):
        raise FileNotFoundError("Could not find destination folder")

    # get replays and sort by recency
    list_of_files = glob.glob(replay_folder + "/*.roa")
    if (len(list_of_files) < number_of_files):
        raise FileNotFoundError("Could not find replays")
    sorted_files = sorted(list_of_files, key=lambda t: -os.stat(t).st_mtime)

    # make set directory
    if (os.path.isdir(target_folder + "\\" + set_name)):
        raise IsADirectoryError("Set directory already exists")
    os.mkdir(target_folder + "\\" + set_name)
    
    #copy files over to set directory
    for i in range(number_of_files):
        file_name = sorted_files[i].split('\\')[-1]
        shutil.copyfile(sorted_files[i], target_folder + "\\" + set_name + "\\" + file_name)

def zip_and_delete_set(set_folder):
    i = 1
    incremented_name = set_folder
    while (os.path.isfile(incremented_name + ".zip")):
        incremented_name = set_folder + "(" + str(i) + ")"
        i += 1
    shutil.make_archive(incremented_name, "zip", set_folder)
    shutil.rmtree(set_folder)

def save(dict):
    with open('config.pkl', 'wb') as file:
        pickle.dump(dict, file, protocol=0)

def load():
    try:
        with open('config.pkl', 'rb') as file:
            dict = pickle.load(file)
            return dict
    except:
        return None

def parse_suggested_set_name(replay_folder):
    if (not os.path.isdir(replay_folder)):
        return ""
    list_of_files = glob.glob(replay_folder + "/*.roa")
    if (len(list_of_files) == 0):
        return ""
    sorted_files = sorted(list_of_files, key=lambda t: -os.stat(t).st_mtime)
    most_recent_roa_file = open(sorted_files[0], 'r')
    roa_text = most_recent_roa_file.readlines()
    regex = re.compile("^H.{32}")
    matches = []
    for line in roa_text:
        match = regex.search(line)
        if (match):
            matches.append(match)
    if (len(matches) < 2):
        return ""
    return matches[0].group(0)[1:].strip() + " vs " + matches[1].group(0)[1:].strip()

