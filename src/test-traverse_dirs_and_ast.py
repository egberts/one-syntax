"""
The Right Stuff
"""
from pathlib import Path
from collections import deque
import construct_symbol_name
import parse_simple_ini

# Define pathspec for directory traversal
INI_DIRPATH = './'
pathspec = Path('./.')  # Define pathspec


def process_terminal_token_end_node(entry, symbol_name, stack):
    """
    :param entry:
    :param symbol_name:
    :param stack:
    """
#    print("  File: %s" % entry.name)
#    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    print("End-node Terminal Symbol Name (file): %s" % symbol_name)

    
def process_node_simple_no_config(parent_entry, entry, symbol_name, stack):
    """

    :param parent_entry:
    :param entry:
    :param symbol_name:
    :param stack:
    """
    #    print("  File: %s" % entry)
    #    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    print("Non-terminal symbol (dir/no-config): %s" % symbol_name)


def start_directory_traverse(start_dir, hidden_prefix=Path("."), prefix='nft_'):
    """

    :param start_dir:
    :param hidden_prefix:
    :param prefix:
    :return:
    """

    def traverse_recursively(path, stack=deque()):
        """

        :param path:
        :param stack:
        """
        stack.append(path)
        # Always pick up config file before recursion
        keyword_config = parse_simple_ini.get_node_options(path)
        try:
            for entry in path.iterdir():
                # Skip hidden files, nft_* files, and config files
                if entry.name.startswith('.'):
                    continue
                if entry.name.startswith(str(hidden_prefix)):
                    continue
                if entry.name.startswith('.config'):
                    continue
                if entry.name.endswith('.nft'):
                    continue

                # Process directories and files appropriately
                if entry.is_dir():
                    traverse_recursively(entry, stack)
                    # Do we really want to check stack size as an exit mechanism for the last outputted symbol name?
                    full_symbol_name = construct_symbol_name.get_dir(stack, prefix)
                    entry_symbol_name = full_symbol_name + '_' + construct_symbol_name.convert(path.name, entry.name)
                    node_options = parse_simple_ini.get_node_options(entry)
                    if not node_options:
                        process_node_simple_no_config(path, entry, entry_symbol_name, stack)
                    else:
                        process_node_simple_no_config(path, entry, entry_symbol_name, stack)
                        #print("Non-terminal symbol (dir/config): %s" % entry_symbol_name)
                elif entry.is_file():
                    # why does 'add' 'add' get added twice?
                    full_symbol_name = construct_symbol_name.get_file(stack, path.name, prefix)
                    process_terminal_token_end_node(entry, full_symbol_name, stack)

        except PermissionError:
            print("  Permission denied: %s" % path.name)
        stack.pop()

        
    # Run start_directory_traverse() with pathspec to its top-level directory
    start_path = Path(start_dir).resolve()  # Convert to Path and resolve
    if start_path.is_file():
        print("Path %s is a file, not a directory; aborted." % start_path.name)
        return
    if not start_path.is_dir():
        print("Path %s is not a directory; aborted." % start_path.name)
        return

    traverse_recursively(start_path)
    # last node traversed here, what's next?

# Run traverse_dirs with pathspec
options = parse_simple_ini.get_main_options(Path(INI_DIRPATH))
symbol_prefix = options.get('symbol_name_prefix', 'nft_')  # Fallback to 'nft_' if not found

# Do top-level differently than rest of tree-traversing
start_directory_traverse(pathspec, symbol_prefix)