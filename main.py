import sys

from processing.hit_commit import hit_commit
from processing.hit_add import hit_add
from processing.hit_status import hit_status
from processing.hit_init import hit_init

if len(sys.argv) == 1:
    print("Hit Semantive version 1.00")
    sys.exit(0)

cmd_dict = {"init": hit_init, "status": hit_status, "add": hit_add,
            "commit": hit_commit}

cmd = sys.argv[1]

try:
    cmd_dict[cmd](sys.argv[2:])
except KeyError:
    print(f"Unrecognized command: {cmd}")
