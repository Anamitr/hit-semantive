import json
import os
from shutil import copy

from util import reset_working_dir


@reset_working_dir
def hit_init():
    hit_dir = ".hit"
    hit_init_files = ["hit", "hit-log"]
    hit_sub_dirs = ["commits"]
    if os.path.exists(hit_dir):
        print(f"Hit repo already initialized at {os.getcwd()}")
        return
    else:
        os.mkdir(hit_dir)
        os.chdir(hit_dir)

        for hit_sub_dir in hit_sub_dirs:
            os.mkdir(hit_sub_dir)

        for file_name in hit_init_files:
            open(file_name, 'a').close()

        file = open('hit', 'w')
        json.dump({"name": "Hit Semantive", "staged": []}, file, indent=4)
        file.close()
        print(f"Initialized empty Hit repository in {os.getcwd()}")


def get_new_files(hit_content: str) -> list:
    dir_content = os.listdir(os.getcwd())
    return [file for file in dir_content if
            file not in hit_content and file != ".hit"]


def read_hit_content(path="") -> dict:
    path = str(path)
    if path and path[-1] != '/':
        path += '/'
    file = open(path + ".hit/hit", 'r')
    result = json.load(file)
    file.close()
    return result


def hit_status():
    hit_content = read_hit_content()
    new_files = get_new_files(str(hit_content))
    [print(f"> {file_name} (staged file)") for file_name in
     hit_content["staged"]]
    [print(f"> {file_name} (new file)") for file_name in new_files]


def save_hit_content(hit_content):
    with open('.hit/hit', 'w') as f:
        json.dump(hit_content, f, indent=4)


def hit_add(file_paths):
    """ file_paths is str or list of str """
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    elif isinstance(file_paths, list):
        pass
    else:
        raise TypeError("file_paths should be str or list of str")

    hit_content = read_hit_content()
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"No such file {file_path}")
        else:
            if file_path not in hit_content["staged"]:
                hit_content["staged"] += [file_path]
    hit_content["staged"] = sorted(hit_content["staged"])
    save_hit_content(hit_content)


def hit_commit():
    hit_content = read_hit_content()
    commits_path = ".hit/commits/"
    os.mkdir(commits_path + "0")
    for staged_file in hit_content["staged"]:
        copy(staged_file, commits_path + "0/")
