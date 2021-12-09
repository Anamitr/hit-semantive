import functools
import os
import sys


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


def no_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args[0]) != 0 or len(kwargs) != 0:
            print(f"{func.__name__.replace('_', ' ')} takes no arguments!")
            sys.exit(1)
        value = func()
        return value

    return wrapper
