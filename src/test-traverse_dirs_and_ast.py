"""
The Right Stuff
"""
from collections import deque
from pathlib import Path

import construct_symbol_name
import parse_simple_ini

highlights_found = []
errors_defined = []

# Define pathspec for directory traversal
INI_DIRPATH = './'
pathspec = Path('./.')  # Define pathspec


highlights_printed = []


def output_vimscript_comment(comment_line: str) -> None:
    """

    :param comment_line:
    :rtype: None
    """
    # iterate and collect name of next keywords
    print("\" %s" % comment_line)


def output_highlights_found() -> None:
    """
    Output a list of highlight group name found in .config.ini files.
    :rtype: None
    """
    output_vimscript_comment(' Highlights found')
    for this_highlight in highlights_found:
        group_name = this_highlight[0]
        label_name = this_highlight[1]
        output_vimscript_comment('  Highlight \'' + label_name +  '\' referenced by ' + group_name)
        if any(group_name not in item[0] for item in highlights_found):
            print('highlight link ' + label_name + ' <fill in>')


def output_error_labels_defined() -> None:
    """
    Output a list of error-related group names
    :rtype: None
    """
    output_vimscript_comment(' Error Handlers encountered')
    for this_error_handler in errors_defined:
        group_name = this_error_handler[0]
        symbol = this_error_handler[1]
        pattern = this_error_handler[2]
        print('syntax match ' + group_name + ' \'' + pattern + '\' contained')


def any_child_node_exists(path: Path) -> bool:
    """

    :param path:
    :return:
    :rtype: bool
    """
    found = False
    for this_child in path.iterdir():
        if this_child.is_dir():
            found = True
            break
    return found


def process_terminal_token_end_node(symbol_name: str) -> None:
    """
    :param symbol_name:
    :rtype: None
    """
    #    print("  File: %s" % entry.name)
    #    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    output_vimscript_comment("End-node Terminal Symbol Name (file): %s" % symbol_name)



def output_vimscript_highlight(group_name: str, highlight_link_label: str) -> None:
    """

    :param group_name:
    :param highlight_link_label:
    :rtype: None
    """
    # iterate and collect name of next keywords
    print("highlight link %s %s" % (group_name, highlight_link_label))
    # print("highlight link %s %s" % (group_name, highlight_link_label))
    # track all highlight group names for later output
    highlights_found.append([ group_name, highlight_link_label])


def output_vimscript_syn_match(path: Path, group_name: str, node_options, non_terminal: bool) -> None:
    """

    :param path:
    :param group_name:
    :param node_options:
    :param non_terminal:
    :rtype: None
    """
    # Use default
    pattern = '\\v' + path.name

    # 'skipwhite' Vimscript syntax option is mostly useless here (only does '\s*' or not)
    # for a deterministic syntax pathway, we default to 'atleastwhitespace' '\s+', so we do this in regex
    if node_options:


        if 'pattern' in node_options:
            option_pattern = node_options['pattern']
            regex_pattern = option_pattern.rstrip('\'').lstrip('\'')
            if non_terminal:
                pattern = '\\v' + regex_pattern
            elif not non_terminal:
                pattern = '\\v' + regex_pattern

        # Pretty much always expect a space after each keyword so make that its default
        minimum_whitespace = ''
        if node_options['squishable_with_next_token']:
            squished_tokens = node_options['squishable_with_next_token']
            if squished_tokens:
                # Also, one other thing: do NOT USE '\s'; use '[ \t]'...  too many syntax options differentiate those
                minimum_whitespace = '[ \\t]{0,5}'
            else:
                minimum_whitespace = '[ \\t]{1,5}'

        pattern = pattern + minimum_whitespace

    # TODO: Root-level keywords do not use 'contained' syntax option in a deterministic pathway design (LL(1))

    print("syntax match %s '%s' contained" % (group_name, pattern))


def output_vimscript_nextgroup(path: Path, group_name: str) -> None:
    """

    :param path:
    :param group_name:
    :rtype: None
    """
    if any_child_node_exists(path):
        print("\\ nextgroup=")
        # compile a list of group labels (store their pattern length/complexity)
        for this_filename in path.iterdir():
            if this_filename.name.startswith('.'):
                continue
            this_keyword = this_filename.name
            this_symbol_name = construct_symbol_name.convert(group_name, this_keyword)
            this_group_name = group_name + '_' + this_symbol_name
            print("\\    %s," % this_group_name)
        # output the length-lexical sort order of group names


def output_vimscript_nextgroup_error_handlers(error_options: list) -> None:
    """

    :param error_options:
    :rtype: None
    """
    if not error_options:
        print('\\    nft_Error')
        return
    if 'follow_on_to_only' not in error_options:
        print('\\    nft_Error')
        return
    follow_on_to_only = error_options['follow_on_to_only']
    #  new_line,end_of_statement,start_block_delimiter,end_block_delimiter,equal,start_parenthesis,end_parenthesis,slash,at_symbol,dot,comma,colon,plus,dash,asterisk

    list_of_foto = follow_on_to_only.split(',')
    # concatenate a list of anti-pattern firstly
    anti_pattern = ''
    #for this_token in list_of_foto:

    if 'equal' in list_of_foto:
        list_of_foto.remove('equal')
        add_on_pattern = '='
        new_error_group_name = symbol_prefix + 'Error_equal_not_found'
        print('\\    %s' % new_error_group_name)
        final_antipattern = r'\v[^' + add_on_pattern + ']'
        errors_defined.append([ new_error_group_name, add_on_pattern, final_antipattern])
        #print('error_defined (running): ', errors_defined)
    # TODO: construct unique error handler
    if not not list_of_foto:
        print('ERROR: remaining unprogrammed follow_on_to_only options: ', list_of_foto)


def process_node_nonterminal(parent_path: Path, path: Path, parent_symbol_name: str, symbol_name: str, stack: object) -> None:
    """

    :param parent_path:
    :type parent_path: Path
    :param path:
    :type path: Path
    :param parent_symbol_name:
    :type parent_symbol_name: str
    :param symbol_name:
    :type symbol_name: str
    :param stack:
    :type stack: object
    :rtype: None
    """
    #    print("  File: %s" % entry)
    #    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    node_options = parse_simple_ini.get_node_options(path)
    if node_options and 'pattern' in node_options:
        pattern = '\\v' + node_options['pattern'].rstrip('\'').lstrip('\'')
        output_vimscript_comment("Non-terminal symbol (dir): ' + symbol_name + ' (has .config.ini; pattern: " + pattern)
    else:
        output_vimscript_comment("Non-terminal symbol (dir): %s" % path.name)
    output_vimscript_comment(path)
    if 'highlight_color_name' in node_options:
        output_vimscript_highlight(symbol_name, node_options['highlight_color_name'])

    # There is a loop here for multiple patterns using exact same group name
    output_vimscript_syn_match(path, symbol_name, node_options, non_terminal=True)
    output_vimscript_nextgroup(path, symbol_name)
    output_vimscript_nextgroup_error_handlers(node_options)
    output_vimscript_comment('')


def process_end_node_terminal(parent_path: Path, path: Path, parent_symbol_name: str, symbol_name: str, stack: object) -> None:
    """

    :param parent_symbol_name:
    :param parent_path:
    :param path:
    :param symbol_name:
    :param stack:
    :rtype: None
    """
    #    print("  File: %s" % entry)
    #    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    pattern = '\\v' + symbol_name  # default pattern
    node_options = parse_simple_ini.get_node_options(path)
    if node_options:
        output_vimscript_comment("Terminal symbol (dir): ' + symbol_name + ' (has .config.ini)")
        if 'pattern' in node_options:
            output_vimscript_comment("(pattern defined)")
        else:
            output_vimscript_comment("(default pattern used)")
    else:
        output_vimscript_comment("Terminal symbol (dir): " + symbol_name)
        
    # There is a loop here for multiple patterns using exact same group name
    output_vimscript_comment(path)
    if 'highlight_color_name' in node_options:
        output_vimscript_highlight(symbol_name, node_options['highlight_color_name'])
    output_vimscript_syn_match(path, symbol_name, node_options, non_terminal=False)
    output_vimscript_comment('')


def start_directory_traverse(start_dir: object, hidden_prefix: Path = Path("."), prefix: str = 'nft_') -> None:
    """

    :return:
    :param start_dir:
    :param hidden_prefix:
    :param prefix:
    :rtype: None
    """

    def traverse_recursively(path: Path, stack = deque()) -> None:
        """

        :param path:
        :param stack:
        :rtype: None
        """
        stack.append(path)
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
                    full_symbol_name = construct_symbol_name.get_dir(stack, prefix)
                    entry_symbol_name = full_symbol_name + '_' + construct_symbol_name.convert(path.name, entry.name)

                    # Lookahead for not non-terminal (terminal) node
                    if any_child_node_exists(entry):
                        process_node_nonterminal(path, entry, full_symbol_name, entry_symbol_name, stack)
                    else:
                        process_end_node_terminal(path, entry, full_symbol_name, entry_symbol_name, stack)
                elif entry.is_file():
                    raise NotADirectoryError('Not sure what to do with this file')  # not sure
                    full_symbol_name = construct_symbol_name.get_file(stack, path.name, prefix)
                    process_terminal_token_end_node(full_symbol_name)

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


# Retrieve options from root 'syntax-tree/.config.main.ini
options = parse_simple_ini.get_main_options(Path(INI_DIRPATH))

# set our first global options
symbol_prefix = options.get('symbol_name_prefix', 'nft_')  # Fallback to 'nft_' if not found

# Do top-level differently than rest of tree-traversing
start_directory_traverse(pathspec, symbol_prefix)

output_highlights_found()
output_error_labels_defined()
