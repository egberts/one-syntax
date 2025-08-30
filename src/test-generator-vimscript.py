"""
Test Vimscript Generator
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


def traverse_dirs(start_dir, hidden_prefix=Path("."), prefix='nft_'):
    """

    :param start_dir:
    :param hidden_prefix:
    :param prefix:
    :return:
    """
    def process_non_terminal_symbol(parent_entry, entry, symbol_name, stack):
        """

        :param parent_entry:
        :param entry:
        :param symbol_name:
        :param stack:
        """
        entry_symbol_name = symbol_name + '_' + construct_symbol_name.convert(parent_entry.name, entry.name)
        node_options = parse_simple_ini.get_node_options(entry)
        if not node_options:
            # it is a simple EBNF symbol
            process_node_simple_no_config(parent_entry, entry, entry_symbol_name, stack)
        else:
            print("Non-terminal symbol (dir/config): %s" % entry_symbol_name)

        recursive_traverse(entry, stack)


    def process_node(path, stack, settings):
        """

        :param path:
        :param stack:
        """
        try:
            for entry in path.iterdir():
                # Hide those dot-files (we can open those later)
                if entry.name.startswith('.'):
                    continue
                # Hide those 'nft_*' files (we can open those later)
                if entry.name.startswith(str(hidden_prefix)):
                    continue
                # Hide those configuration files
                if entry.name.startswith('.config'):
                    continue
                full_symbol_name = construct_symbol_name.get(stack, prefix)
                if entry.is_file():
                    process_terminal_token_end_node(entry, full_symbol_name, stack)

                elif entry.is_dir():
                    process_non_terminal_symbol(path, entry, full_symbol_name, stack)

        except PermissionError:
            print("  Permission denied: %s" % path.name)
        stack.pop()

    def recursive_traverse(path, stack=deque()):
        """

        :param path:
        :param stack:
        """
        stack.append(path)
        keyword_config = parse_simple_ini.get_node_options(path)
        process_node(path, stack, keyword_config)


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
symbol_prefix = options.get('symbol_name_prefix', 'nft_')  # Fallback to 'nft_' if not found
traverse_dirs(pathspec, symbol_prefix)