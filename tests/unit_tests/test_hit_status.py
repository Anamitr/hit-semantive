import os
import subprocess

from processing.hit_add import hit_add
from processing.hit_commit import hit_commit
from processing.hit_init import hit_init
from processing.hit_status import hit_status


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


def test_hit_status_after_modifying_committed_file(repo_with_3_files, capsys):
    """ GIVEN repository with one new, one committed and one committed
              and modified file
        WHEN hit_status() is called
        THEN info about one modified and one new file should be displayed
    """
    hit_init()
    hit_add("file1")
    hit_add("file2")
    hit_commit()
    subprocess.run("echo 'test' >> file2", shell=True)
    capsys.readouterr().out = ""

    hit_status()
    out = capsys.readouterr().out
    assert "file1" not in out
    assert "> file2 (modified file)" in out
    assert "> file3 (new file)" in out