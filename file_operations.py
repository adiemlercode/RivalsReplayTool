from datetime import date
import glob
import os
import pickle
import re
import shutil

steam_name_regex = re.compile("^H.{32}")

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

def get_sorted_replays(replay_folder):
    if (not os.path.isdir(replay_folder)):
        return []
    list_of_files = glob.glob(replay_folder + "/*.roa")
    if (len(list_of_files) == 0):
        return []
    return sorted(list_of_files, key=lambda t: -os.stat(t).st_mtime)

def get_steam_name_matches(roa_file):
    opened_roa_file = open(roa_file, 'r')
    roa_text = opened_roa_file.readlines()
    matches = []
    for line in roa_text:
        match = steam_name_regex.search(line)
        if (match):
            matches.append(match)
    return matches

def parse_suggested_set_name(replay_folder):
    sorted_files = get_sorted_replays(replay_folder)
    if (len(sorted_files) == 0):
        return ""
    matches = get_steam_name_matches(sorted_files[0])
    if (len(matches) < 2):
        return ""
    set_name = matches[0].group(0)[1:].strip() + " vs " + matches[1].group(0)[1:].strip()
    # Parse out nonalphanumeric characters for filename
    set_name = re.sub('[^\w_.)( -]', '', set_name)
    return set_name

def parse_suggested_game_count(replay_folder):
    sorted_files = get_sorted_replays(replay_folder)
    if (len(sorted_files) == 0):
        return ""
    matches = get_steam_name_matches(sorted_files[0])
    if (len(matches) < 2):
        return ""
    player_one = matches[0].group(0)[1:].strip()
    player_two = matches[1].group(0)[1:].strip()
    games = 1
    range_max = min(len(sorted_files), 5)
    for i in range(1, range_max):
        matches = get_steam_name_matches(sorted_files[i])
        same_players = matches[0].group(0)[1:].strip() == player_one and matches[1].group(0)[1:].strip() == player_two
        if (same_players):
            games += 1
        else:
            break
    return games


