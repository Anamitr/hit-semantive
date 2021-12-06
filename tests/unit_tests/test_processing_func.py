import os
import subprocess

from hit_processing.processing_func import hit_init, hit_status


def test_hit_init(test_dir, capsys):
    """ GIVEN temp directory
        WHEN hit init is called
        THEN .hit file should exist and msg displayed
    """
    hit_init()

    dir_content = os.listdir(test_dir)
    out = capsys.readouterr().out
    assert ".hit" in dir_content
    assert f"Initialized empty Hit repository in {test_dir}" in out


def test_hit_init_double(test_dir, capsys):
    """ GIVEN temp directory
        WHEN hit init is called twice
        THEN .hit file should exist and msg about repo already initialized
        displayed
    """
    hit_init()
    hit_init()

    dir_content = os.listdir(test_dir)
    out = capsys.readouterr().out
    assert ".hit" in dir_content
    assert f"Initialized empty Hit repository in {test_dir}" in out
    assert f"Hit repo already initialized at {test_dir}" in out


def test_hit_status_new_file(test_dir, capsys):
    """ GIVEN directory with files not added to hit
        WHEN hit_status() is called
        THEN should display list of new files
    """
    subprocess.run("touch file1 ; touch file2", shell=True)
    dir_content = os.listdir(test_dir)
    assert "file1" in dir_content and "file2" in dir_content

    hit_init()
    hit_status()

    out = capsys.readouterr().out
    assert "> file1 (new file)" in out
    assert "> file2 (new file)" in out
