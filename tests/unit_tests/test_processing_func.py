import os
import subprocess

from hit_processing.processing_func import hit_status, hit_add, \
    read_hit_content, hit_commit
from hit_processing.hit_init import hit_init


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


def test_hit_commit_first(repo_with_3_files, capsys):
    """ GIVEN hit repository with some staged files
        WHEN hit_commit is called
        THEN staged files should be copied to commit dir
             and hit status should not show them
    """
    hit_init()
    hit_add("file2")
    hit_add("file3")

    hit_commit()

    commits_path = str(repo_with_3_files) + "/.hit/commits"
    commit_dirs = os.listdir(commits_path)
    assert "1" in commit_dirs
    commit_files = os.listdir(commits_path + "/1")
    assert "file2" in commit_files
    assert "file3" in commit_files

    capsys.readouterr().out = ""
    hit_status()
    out = capsys.readouterr().out
    assert "> file1 (new file)" in out
    assert "file2" not in out
    assert "file3" not in out


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


def test_hit_commit_second(repo_with_3_files, capsys):
    """ GIVEN repository with a commit
        WHEN some changes are added and hit_commit() called
        THEN new commit should be created and hit_status() updated"""
    hit_init()
    hit_add("file1")
    hit_add("file2")
    hit_commit()
    subprocess.run("echo 'test' >> file2", shell=True)
    capsys.readouterr().out = ""

    hit_add("file2")
    hit_commit()

    commits_path = str(repo_with_3_files) + "/.hit/commits"
    commit_dirs = os.listdir(commits_path)
    assert "2" in commit_dirs
    first_commit_files = os.listdir(commits_path + "/1")
    assert first_commit_files == ["file1", "file2"]
    second_commit_files = os.listdir(commits_path + "/2")
    assert second_commit_files == ["file2"]
    file2_old = open(commits_path + "/1/file2", 'r').read()
    file2_new = open(commits_path + "/2/file2", 'r').read()
    assert file2_old != file2_new
