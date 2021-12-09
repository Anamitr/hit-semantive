# Hit Semantive

This project was created as a recruitment task. Its aim is to simulate basic
git functionalities.

### Install

For installation use install.sh. It will copy necessary files to ~/.hit_install
and add it to path in ~/.bashrc. Create new terminal or source ~/.bashrc to
use.

Developed and tested on WSL Ubuntu 20.04.3 LTS, Python 3.8.8. Other version of
Linux and Python should also work but weren't tested.

### Usage

- hit init - initialize hit repository. Create .hit directory for config and
  commit files.
- hit status - display status of repository. Identify 4 types of files:
    - new file - created and not added
    - staged - created or modified and added
    - modified - present in last commit, but modified
    - unmodified - present in last commit and not modified (won't be displayed)
- hit add - stages new or modified file.
- hit commit - creates new commit, copying all staged files to internal commit
  dir. Further modifications will be compared to these files.

### Tests

Run `pytest` in main directory. There are unit tests and one longer integration
test containing script from email description. You can also run manual_tests
scripts yourself.

### Requirements

- Python 3
- pytest