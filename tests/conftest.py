import os
import subprocess

from pytest import fixture

from hit_processing.processing_func import hit_init


@fixture
def test_dir(tmp_path):
    os.chdir(tmp_path)
    return tmp_path


@fixture
def repo_with_3_files(test_dir):
    hit_init()
    subprocess.run("touch file1; touch file2; touch file3", shell=True)
    return test_dir
