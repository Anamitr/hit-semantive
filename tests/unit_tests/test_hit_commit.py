import os
import subprocess

from processing.hit_add import hit_add
from processing.hit_commit import hit_commit
from processing.hit_init import hit_init
from processing.hit_status import hit_status


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


def test_hit_commit_second(repo_with_3_files, capsys):
    """ GIVEN repository with a commit
        WHEN some changes are added and hit_commit() called
        THEN new commit should be created and hit_status() updated
    """
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