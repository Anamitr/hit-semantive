import os
from shutil import copy2

from hit_processing.processing_func import read_hit_content, save_hit_content
from util import no_args


@no_args
def hit_commit():
    hit_content = read_hit_content()
    commits_path = ".hit/commits/"
    hit_content["lastCommit"] += 1
    os.mkdir(commits_path + str(hit_content["lastCommit"]))
    for staged_file in hit_content["staged"]:
        copy2(staged_file, commits_path + f"{hit_content['lastCommit']}/")
    hit_content["staged"] = []
    save_hit_content(hit_content)
