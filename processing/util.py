import os


def subtract_lists(list1: list, list2: list) -> list:
    return [item for item in list1 if item not in list2]


def touch_files(files: list):
    for file_name in files:
        open(file_name, 'a').close()


def create_dirs(sub_dirs: list):
    for sub_dir in sub_dirs:
        os.mkdir(sub_dir)
