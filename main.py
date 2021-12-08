import sys

from hit_processing.processing_func import hit_init, hit_status, hit_add, \
    hit_commit

if len(sys.argv) == 1:
    print("Hit Semantive version 0.01")
    sys.exit(0)

cmd = sys.argv[1]
if cmd == "init":
    hit_init()
elif cmd == "status":
    hit_status()
elif cmd == "add":
    hit_add(sys.argv[2:])
elif cmd == "commit":
    hit_commit()
else:
    print(f"Unrecognized command: {cmd}")
