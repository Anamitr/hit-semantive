import os

from hit_processing.processing_func import read_hit_content
from util import no_args, subtract_lists


def get_new_files(hit_content: str) -> list:
    dir_content = os.listdir(os.getcwd())
    return [file for file in dir_content if
            file not in hit_content and file != ".hit"]


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
