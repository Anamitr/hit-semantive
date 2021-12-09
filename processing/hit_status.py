import os

from processing.hit_processing import read_hit_content, \
    get_staged_new_modified_files
from processing.decorators import no_args


def get_new_files(hit_content: str) -> list:
    dir_content = os.listdir(os.getcwd())
    return [file for file in dir_content if
            file not in hit_content and file != ".hit"]


def get_committed_files(hit_content: dict) -> list:
    files_in_last_commit = os.listdir(
        f"./hit/commits/{hit_content['lastCommit']}")
    current_files = os.listdir('.')
    return list({*current_files, *files_in_last_commit})


@no_args
def hit_status():
    hit_content = read_hit_content()
    staged_files, new_files, modified_files = \
        get_staged_new_modified_files(hit_content)

    [print(f"> {file_name} (staged file)") for file_name in
     hit_content["staged"]]
    [print(f"> {file_name} (modified file)") for file_name in modified_files]
    [print(f"> {file_name} (new file)") for file_name in new_files]
    if not (hit_content["staged"] or modified_files or new_files):
        print("> ")

    return hit_content["staged"], modified_files, new_files
