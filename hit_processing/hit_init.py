import json
import os

from util import reset_working_dir, no_args, touch_files, create_dirs


@reset_working_dir
@no_args
def hit_init():
    hit_dir = ".hit"
    hit_init_files = ["hit", "hit-log"]
    hit_sub_dirs = ["commits", "commits/0"]

    if os.path.exists(hit_dir):
        print(f"Hit repo already initialized at {os.getcwd()}")
        return
    else:
        os.mkdir(hit_dir)
        os.chdir(hit_dir)

        create_dirs(hit_sub_dirs)

        touch_files(hit_init_files)

        init_hit_main_config()
        print(f"Initialized empty Hit repository in {os.getcwd()}")


def init_hit_main_config():
    file = open('hit', 'w')
    json.dump({"name": "Hit Semantive", "staged": [], "lastCommit": 0},
              file, indent=4)
    file.close()
