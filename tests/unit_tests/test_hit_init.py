import os

from processing.hit_init import hit_init


def test_hit_init(test_dir, capsys):
    """ GIVEN temp directory
        WHEN hit init is called
        THEN .hit file should exist and msg displayed
    """
    hit_init()

    dir_content = os.listdir(test_dir)
    hit_dir_content = os.listdir(str(test_dir) + '/.hit')
    out = capsys.readouterr().out
    assert ".hit" in dir_content
    assert "hit" in hit_dir_content
    assert "hit-log" in hit_dir_content
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