import os
import subprocess

from main import hit_init


def test_hit_init(tmp_path, capsys):
    """ GIVEN temp directory
        WHEN hit init is called
        THEN .hit file should exist and msg displayed
    """
    os.chdir(tmp_path)

    hit_init()

    dir_content = os.listdir(tmp_path)
    out = capsys.readouterr().out
    assert ".hit" in dir_content
    assert f"Initialized empty Hit repository in {tmp_path}" in out


def test_hit_init_double(tmp_path, capsys):
    """ GIVEN temp directory
        WHEN hit init is called twice
        THEN .hit file should exist and msg about repo already initialized
        displayed
    """
    os.chdir(tmp_path)

    hit_init()
    hit_init()

    dir_content = os.listdir(tmp_path)
    out = capsys.readouterr().out
    assert ".hit" in dir_content
    assert f"Initialized empty Hit repository in {tmp_path}" in out
    assert f"Hit repo already initialized at {tmp_path}" in out
