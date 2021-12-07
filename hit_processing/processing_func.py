import json
import os

from util import reset_working_dir


@reset_working_dir
def hit_init():
    hit_dir = ".hit"
    hit_init_files = ["hit", "hit-log"]
    if os.path.exists(hit_dir):
        print(f"Hit repo already initialized at {os.getcwd()}")
        return
    else:
        os.mkdir(hit_dir)
        os.chdir(hit_dir)
        for file_name in hit_init_files:
            file = open(file_name, 'w')
            json.dump({"name": "Hit Semantive", "staged": []}, file)
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
    [print(f"> {file_name} (new file)") for file_name in new_files]


def save_hit_content(hit_content):
    with open('.hit/hit', 'w') as f:
        json.dump(hit_content, f, indent=4)


def hit_add_all():
    hit_content = read_hit_content()
    files = os.listdir(os.getcwd())
    staged_set = set(hit_content["staged"] + files)
    staged_set.remove('.hit')
    hit_content["staged"] = sorted(list(staged_set))
    save_hit_content(hit_content)


def hit_add(file_path: str):
    if file_path == '*':
        hit_add_all()
        return

    if not os.path.exists(file_path):
        print(f"No such file {file_path}")
    else:
        hit_content = read_hit_content()
        if file_path not in hit_content["staged"]:
            hit_content["staged"] += [file_path]
        save_hit_content(hit_content)
