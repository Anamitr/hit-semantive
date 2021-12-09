import json
import os
from shutil import copy2

from util import no_args


def read_hit_content(path="") -> dict:
    path = str(path)
    if path and path[-1] != '/':
        path += '/'
    file = open(path + ".hit/hit", 'r')
    result = json.load(file)
    file.close()
    return result


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
