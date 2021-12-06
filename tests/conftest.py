import os

from pytest import fixture


@fixture
def test_dir(tmp_path):
    os.chdir(tmp_path)
    return tmp_path
