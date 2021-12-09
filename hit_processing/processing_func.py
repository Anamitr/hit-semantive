import json
import os
from shutil import copy, copyfile, copy2

from util import reset_working_dir, subtract_lists, no_args


@reset_working_dir
@no_args
def hit_init():
    hit_dir = ".hit"
    hit_init_files = ["hit", "hit-log"]
    hit_sub_dirs = ["commits", "commits/0"]
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
        json.dump({"name": "Hit Semantive", "staged": [], "lastCommit": 0},
                  file, indent=4)
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


def get_committed_files(hit_content: dict) -> list:
    files_in_last_commit = os.listdir(
        f"./hit/commits/{hit_content['lastCommit']}")
    current_files = os.listdir('.')
    return list({*current_files, *files_in_last_commit})


def get_files_from_last_commit(hit_content):
    return os.listdir(f"./.hit/commits/{hit_content['lastCommit']}")


def is_file_modified(file: str, hit_content: dict) -> bool:
    file_content = open(file, 'r').read()
    last_commit_file_content = open(
        f".hit/commits/{hit_content['lastCommit']}/{file}", 'r').read()
    return file_content != last_commit_file_content


@no_args
def hit_status():
    hit_content = read_hit_content()
    new_files, modified_files, unmodified_files = [], [], []
    files_in_last_commit = get_files_from_last_commit(hit_content)
    current_files = subtract_lists(os.listdir("."), hit_content["staged"])
    current_files = subtract_lists(current_files, [".hit"])

    for current_file in current_files:
        if current_file not in files_in_last_commit:
            new_files.append(current_file)
        else:
            if is_file_modified(current_file, hit_content):
                modified_files.append(current_file)
            else:
                unmodified_files.append(current_file)

    [print(f"> {file_name} (staged file)") for file_name in
     hit_content["staged"]]
    [print(f"> {file_name} (modified file)") for file_name in modified_files]
    [print(f"> {file_name} (new file)") for file_name in new_files]
    if not (hit_content["staged"] or modified_files or new_files):
        print("> ")


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


@no_args
def hit_commit():
    hit_content = read_hit_content()
    commits_path = ".hit/commits/"
    hit_content["lastCommit"] += 1
    os.mkdir(commits_path + str(hit_content["lastCommit"]))
    for staged_file in hit_content["staged"]:
        copy2(staged_file, commits_path + f"{hit_content['lastCommit']}/")
    hit_content["staged"] = []
    save_hit_content(hit_content)
