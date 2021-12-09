import subprocess

from processing.hit_add import hit_add
from processing.hit_init import hit_init
from processing.hit_processing import read_hit_content


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