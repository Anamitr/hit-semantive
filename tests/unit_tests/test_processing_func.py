import os
import subprocess

from hit_processing.processing_func import hit_init, hit_status, hit_add, \
    read_hit_content


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


def test_hit_status_new_file(test_dir, capsys):
    """ GIVEN directory with files not added to hit
        WHEN hit_status() is called
        THEN should display list of new files
    """
    subprocess.run("touch file1 ; touch file2", shell=True)
    dir_content = os.listdir(test_dir)
    assert "file1" in dir_content and "file2" in dir_content

    hit_init()
    capsys.readouterr().out = ""
    hit_status()

    out = capsys.readouterr().out
    assert "> file1 (new file)" in out
    assert "> file2 (new file)" in out
    assert ".hit" not in out


def test_hit_add_invalid_file(test_dir, capsys):
    """ GIVEN empty initialized hit repository
        WHEN hit_add(file) is called on non existing file
        THEN should print error msg
    """
    hit_init()

    file_path = "invalid_file.txt"
    hit_add(file_path)

    assert f"No such file {file_path}" in capsys.readouterr().out


def test_hit_add_existing_file(test_dir):
    """ GIVEN hit repository with file
        WHEN hit_add(file) is called
        THEN it's name should be stored in hit as staged
    """
    hit_init()
    subprocess.run("touch file1", shell=True)

    hit_add("file1")

    hit_content = read_hit_content(test_dir)
    assert "file1" in hit_content["staged"]


def test_hit_add_already_added_file(test_dir):
    """ GIVEN hit repository with staged file
        WHEN hit_add(file) is called on staged file
        THEN hit_content shouldn't change
    """
    hit_init()
    subprocess.run("touch file1", shell=True)

    hit_add("file1")
    hit_content_1 = read_hit_content(test_dir)
    hit_add("file1")
    hit_content_2 = read_hit_content(test_dir)

    assert hit_content_1 == hit_content_2


def test_hit_add_multiple(test_dir):
    """ GIVEN hit repository with multiple new files
        WHEN hit_add(files) is called
        THEN all new files should be staged
    """
    hit_init()
    subprocess.run("touch file1; touch file2; touch file3", shell=True)
    files = ["file1", "file2", "file3"]
    hit_add("file1")

    hit_add(files)
    hit_content = read_hit_content(test_dir)

    assert hit_content["staged"] == ["file1", "file2", "file3"]


def test_hit_status_show_staged(test_dir, capsys):
    """ GIVEN hit repository with some staged files
        WHEN hit_status is called
        THEN should display staged files
    """
    hit_init()
    subprocess.run("touch file1; touch file2; touch file3", shell=True)
    hit_add("file1")
    hit_add("file2")
    capsys.readouterr().out = ""

    hit_status()

    out = capsys.readouterr().out
    assert "> file1 (staged file)" in out
    assert "> file2 (staged file)" in out
    assert "> file3 (new file)" in out
