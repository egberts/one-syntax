from pathlib import Path
from collections import deque

pathspec = Path('./.')  # Define pathspec

from pathlib import Path
from collections import deque

# Define pathspec for directory traversal
pathspec = Path('./.')  # Define pathspec


def construct_symbol_name(stack):
    # Start with the prefix
    prefix = 'nft_'

    # If stack has only one entry (root), return prefix
    if len(stack) <= 1:
        return prefix

    # Convert names to snake_case, excluding first entry
    names = []
    for item in list(stack)[1:]:
        camel_case_name = item.name.replace(' ', '_')
        names.append(snake_case_name)

    # Join names with underscores and append to prefix
    return prefix + '_'.join(names)


def traverse_dirs(start_dir, hidden_prefix=Path(".")):
    start_path = Path(start_dir).resolve()  # Convert to Path and resolve
    if not start_path.is_dir():
        print(f"Path {start_path.name} is not a directory; aborted.")
        return
    if start_path.is_file():
        print(f"Path {start_path.name} is a file, not a directory; aborted.")
        return

    def recursive_traverse(path, stack=deque()):
        stack.append(path)
        # Print stack contents, skipping the first entry if stack has more than one
        print(f"Stack Contents: {[p.name for p in list(stack)[1:]] if len(stack) > 1 else []}")
        print(f"Symbol Name: {construct_symbol_name(stack)}")
        print(f"Current Directory: {path.name}")
        try:
            for entry in path.iterdir():
                if entry.name.startswith(str(hidden_prefix)):
                    continue
                if entry.is_file():
                    print(f"  File: {entry.name}")
                elif entry.is_dir():
                    recursive_traverse(entry, stack)
        except PermissionError:
            print(f"  Permission denied: {path.name}")
        stack.pop()

    recursive_traverse(start_path)


# Run traverse_dirs with pathspec
traverse_dirs(pathspec)