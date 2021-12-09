import os
from shutil import copy2

from processing.hit_processing import read_hit_content, save_hit_content
from processing.decorators import no_args


@no_args
def hit_commit():
    hit_content = read_hit_content()
    commits_path = ".hit/commits/"
    last_commit_path = commits_path + str(hit_content["lastCommit"])
    hit_content["lastCommit"] += 1
    new_commit_path = commits_path + str(hit_content["lastCommit"])
    os.mkdir(new_commit_path)
    # Copy all already committed files
    for file in os.listdir(last_commit_path):
        copy2(file, new_commit_path)
    for staged_file in hit_content["staged"]:
        copy2(staged_file, new_commit_path)
    hit_content["staged"] = []
    save_hit_content(hit_content)
