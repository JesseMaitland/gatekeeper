from argparse import Namespace
from gatekeeper.project.file_manager import (
    STAGING_FILE_PATH,
    read_head_file,
    write_head_file,
    hash_file,
    write_commit,
    update_index
)

"""

1. get staged file
2. hash staged file
3. compare with head hash
    if the same, nothing to do.... otherwise
4. make commit file
5. update head

"""


def commit(cmd: Namespace) -> None:

    print("committing staged changes to gatekeeper commit store.")

    if len(STAGING_FILE_PATH.read_text()) == 0:
        print("nothing to stage!")
        return

    staged_hash = hash_file(STAGING_FILE_PATH, 'commit')
    head_hash = read_head_file()

    if head_hash == staged_hash:
        print("staging file has already been committed. Nothing new to stage!")
        return

    message = input("please enter a message... ")
    write_commit(STAGING_FILE_PATH, message)
    write_head_file(staged_hash)
    update_index(staged_hash)

    # now clear out whatever is in staging
    STAGING_FILE_PATH.unlink()
    STAGING_FILE_PATH.touch()
