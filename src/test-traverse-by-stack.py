import os
from pathlib import Path
from collections import deque

pathspec = Path('./.')

def traverse_dirs(start_dir):
    stack = deque([start_dir])
    while stack:
        path = stack.pop()
        print(f"Directory: {path}")
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    # skip hidden file
                    if entry.name.startswith('.'):  # Skip hidden files and directories
                        continue
                    if entry.is_file():
                        print(f"  File: {entry.path}")
                    elif entry.is_dir():
                        stack.append(entry.path)
                    else:
                        print(f"WARNING:  Unknown: {entry.path}")
        except PermissionError:
            print(f"  Permission denied: {path}")

if not pathspec.is_dir():
    print(f"Path {pathspec} is not a directory; aborted.")
    exit(1)
elif pathspec.is_file():
    print(f"Path {pathspec} is not a file; aborted.")
    exit(1)
traverse_dirs(pathspec)