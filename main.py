import os
import sys


def hit_init():
    hit_file_name = ".hit"
    if os.path.exists(hit_file_name):
        print(f"Hit repo already initialized at {os.getcwd()}")
        return
    file = open(hit_file_name, "w")
    file.write("# Hit Semantive file")
    file.close()
    print(f"Initialized empty Hit repository in {os.getcwd()}")


print("Hi Semantive")
