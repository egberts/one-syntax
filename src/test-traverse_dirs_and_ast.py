from pathlib import Path
from collections import deque
import construct_symbol_name
import parse_simple_ini

# Define pathspec for directory traversal
INI_DIRPATH = './'
pathspec = Path('./.')  # Define pathspec


def process_terminal_token_symbol(entry, symbol_name, stack):
#    print("  File: %s" % entry.name)
#    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    print("Terminal Symbol Name (file): %s" % symbol_name)

    
def process_simple_non_terminal(parent_entry, entry, symbol_name, stack):
#    print("  File: %s" % entry)
#    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    print("Non-terminal Name (dir/no-config): %s" % symbol_name)


def traverse_dirs(start_dir, hidden_prefix=Path("."), prefix='nft_'):


    def process_non_terminal(parent_entry, entry, symbol_name, stack):
        options = parse_simple_ini.get_node_options(entry)
        if not options:
            # it is a simple EBNF symbol
            process_simple_non_terminal(parent_entry, entry, symbol_name, stack)
        else:
            print("Non-terminal Name (dir/config): %s" % symbol_name)

        entry_symbol_name = symbol_name + '_' + construct_symbol_name.convert(parent_entry.name, entry.name)
        recursive_traverse(entry, stack)


    def process_node(path, stack):
        """

        :param path:
        :param stack:
        """
        try:
            for entry in path.iterdir():
                if entry.name.startswith(str(hidden_prefix)):
                    continue
                if entry.name == 'config':
                    continue
                full_symbol_name = construct_symbol_name.get(stack, prefix)
                if entry.is_file():
                    process_terminal_token_symbol(entry, full_symbol_name, stack)

                elif entry.is_dir():
                    process_non_terminal(path, entry, full_symbol_name, stack)

        except PermissionError:
            print("  Permission denied: %s" % path.name)
        stack.pop()

    def recursive_traverse(path, stack=deque()):
        stack.append(path)
        keyword_config = parse_simple_ini.get_node_options(path)
        if keyword_config:
            print("%s config found: %s" % (path, keyword_config))
        process_node(path, stack)


    start_path = Path(start_dir).resolve()  # Convert to Path and resolve
    if not start_path.is_dir():
        print("Path %s is not a directory; aborted." % start_path.name)
        return
    if start_path.is_file():
        print("Path %s is a file, not a directory; aborted." % start_path.name)
        return
    recursive_traverse(start_path)

# Run traverse_dirs with pathspec
options = parse_simple_ini.get_main_options(Path(INI_DIRPATH))
prefix = options.get('symbol_name_prefix', 'nft_')  # Fallback to 'nft_' if not found
traverse_dirs(pathspec, prefix=prefix)