import json
import os

from processing.util import subtract_lists


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


def is_file_modified(file: str, hit_content: dict) -> bool:
    file_content = open(file, 'r').read()
    last_commit_file_content = open(
        f".hit/commits/{hit_content['lastCommit']}/{file}", 'r').read()
    return file_content != last_commit_file_content


def get_staged_new_modified_files(hit_content: dict) -> tuple:
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
    return hit_content["staged"], new_files, modified_files


def get_files_from_last_commit(hit_content):
    return os.listdir(f"./.hit/commits/{hit_content['lastCommit']}")