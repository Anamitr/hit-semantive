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
