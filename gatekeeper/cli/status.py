from argparse import Namespace

from gatekeeper.project.file_manager import (
    read_head_file,
    hash_file,
    STAGING_FILE_PATH
)


def status(cmd: Namespace) -> None:
    #TODO: make status a little smarter

    head = read_head_file()
    stage = hash_file(STAGING_FILE_PATH, 'commit')

    if head and STAGING_FILE_PATH.read_text() and (head != stage):
        print("There are uncommitted changes in the staged file.")
    else:
        print("Nothing to stage. Commits are up to date.")
