import functools
import os


def reset_working_dir(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        working_dir = os.getcwd()
        value = func(*args, **kwargs)
        os.chdir(working_dir)
        return value

    return wrapper


def subtract_lists(list1: list, list2: list) -> list:
    return [item for item in list1 if item not in list2]
