import sys

from hit_processing.processing_func import hit_status, hit_add, \
    hit_commit
from hit_processing.hit_init import hit_init

if len(sys.argv) == 1:
    print("Hit Semantive version 0.01")
    sys.exit(0)

cmd_dict = {"init": hit_init, "status": hit_status, "add": hit_add,
            "commit": hit_commit}

cmd = sys.argv[1]

try:
    cmd_dict[cmd](sys.argv[2:])
except KeyError:
    print(f"Unrecognized command: {cmd}")
