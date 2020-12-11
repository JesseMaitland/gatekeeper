from argparse import Namespace
from gatekeeper.project.file_manager import (
    read_index,
    fetch_commit,
    move_commit_to_executed,
    parse_commit

)

"""
1. read the index
2. for each index entry
    3. get the commit file
    4. run the file
    5. move the file to "executed"

6. if everything ran ok, then clear commits, clear index, clear head, clear stage    
"""

def up(cmd: Namespace) -> None:

    for entry in read_index():
        commit = fetch_commit(entry)
        print(parse_commit(commit))


