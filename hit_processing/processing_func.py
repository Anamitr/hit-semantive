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
            file.write("# Hit Semantive file")
            file.close()
        print(f"Initialized empty Hit repository in {os.getcwd()}")


def get_new_files(hit_content: str) -> list:
    dir_content = os.listdir(os.getcwd())
    return [file for file in dir_content if
            file not in hit_content and file != ".hit"]


def read_hit_content() -> str:
    return open(".hit/hit", 'r').read()


def hit_status():
    hit_content = read_hit_content()
    new_files = get_new_files(hit_content)
    [print(f"> {file_name} (new file)") for file_name in new_files]


def hit_add(file_path: str):
    if not os.path.exists(file_path):
        print(f"No such file {file_path}")
