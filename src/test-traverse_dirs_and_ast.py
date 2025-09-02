"""
The Right Stuff
"""
from argparse import ArgumentTypeError
from collections import deque
from collections.abc import Sized
from pathlib import Path
from typing import cast, Set, Dict, Optional, Any, Deque, List, Tuple

import construct_symbol_name
import parse_simple_ini


target_symbol_prefix:str  = ''
target_file_format:str  = ''
TARGET_EDITOR_PLATFORM:str = 'vim'
target_error_defined: List[Tuple[str, str, str]] = []
target_highlights_found: Set[Optional[str]] = set()
target_highlights_printed = []
target_corpus_fileformat_tree_dirpath:Path = Path('.')

# Define pathspec for directory traversal
CORPUS_SYNTAX_TREE_DIRPATH = '/home/wolfe/work/github/one-syntax/'

def is_root_node(stack: Sized) -> bool:
    """
    Check if a node is the root of the syntax tree
    :param stack:
    :rtype: bool
    :return: Returns True if a given node is the tree root
    """
    if len(stack) == 1:
        return True
    return False

def output_vimscript_comment(comment_line: str) -> None:
    """
    Generate a Vimscript comment line
    :param comment_line:
    :ptype comment_line: str
    :rtype: None
    """
    # iterate and collect name of next keywords
    print("\" %s" % comment_line)


def output_highlights_found() -> None:
    """
    Output a list of highlight group name found in all the
    .config.ini files of a syntax tree.
    Output each line as a definition statement in Vimscript
    :rtype: None
    """
    output_vimscript_comment('Highlights found:')
    if target_highlights_found:
        have_target_highlights = cast(Set[str], target_highlights_found)
        for this_highlight in have_target_highlights:
            group_name = this_highlight[0]
            label_name = this_highlight[1]
            referenced_by = this_highlight[2]
            output_vimscript_comment('  Highlight \'' + group_name +  '\' referenced by ' + referenced_by)
            if any(group_name not in item[0] for item in have_target_highlights):
                print('highlight link ' + group_name + ' ' + label_name)

def output_vimscript_highlight_defaults(syntax_tree_path: Path) -> None:

    def collect_all_highlights(syntax_tree: Path) -> Set[Optional[str]]:
        """
        Read a specific key from all '.config.ini' files in subdirectories.
        Handles non-standard INI files without sections.
        Returns a dictionary mapping file paths to the key's value (or None if not found).
        :return:
        """
        key_name:str = "highlight_color_name"
        set_of_default_highlights: Set[Optional[str]] = set()

        # Find all .config.ini files in subdirectories
        for config_file in syntax_tree.rglob(".config.ini"):
            try:
                with open(config_file, 'r') as f:
                    for line in f:
                        # Skip comments and empty lines
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        # Split on first '=' to handle values containing '='
                        if '=' in line:
                            k, v = map(str.strip, line.split('=', 1))
                            if k == key_name:
                                # Store non-duplicative encounters
                                set_of_default_highlights.add(v)
                                break
            except (IOError, UnicodeDecodeError):
                pass
        return set_of_default_highlights

    def output_highlight_default_links_found(default_highlights: Set[str], prefix: str) -> None:
        for this_hi in default_highlights:
            system_highlight = this_hi
            highlight_prefix = prefix.rstrip('_') + 'HL_'
            platform_specific_highlight = highlight_prefix + this_hi
            print(f"highlight default link {platform_specific_highlight} {system_highlight}")

    list_of_default_highlights = collect_all_highlights(syntax_tree_path)
    # Filter out None values to ensure type is Set[str]
    filtered_highlights: Set[str] = {x for x in list_of_default_highlights if x is not None}
    output_highlight_default_links_found(filtered_highlights, target_symbol_prefix)
    return


def output_error_labels_defined() -> None:
    """
    Output a list of error-related group names
    :rtype: None
    """
    output_vimscript_comment(' Error Handlers encountered')
    for this_error_handler in target_error_defined:
        group_name = this_error_handler[0]
        # symbol = this_error_handler[1]
        pattern = this_error_handler[2]
        print('syntax match ' + group_name + ' \'' + pattern + '\' contained')


def any_child_node_exists(node_path: Path) -> bool:
    """
    Check a node if any child node exists.
    :param node_path: a filepath to a node
    :ptype path: Path
    :return: Returns True if a child node exists.
    :rtype: bool
    """
    found = False
    for this_child in node_path.iterdir():
        # we are looking for ordinary (non-block) child nodes
        if not this_child.name.startswith('block_'):
            if this_child.is_dir():
                found = True
                break
    return found

def any_block_related_child_node_exists(node_path: Path) -> bool:
    """
    Check a node if any block-related child node exists.
    :param node_path: a filepath to a node
    :ptype path: Path
    :return: Returns True if a child node exists.
    :rtype: bool
    """
    found = False
    for this_child in node_path.iterdir():
        # we are only looking for block-related child nodes
        if this_child.name.startswith('block_'):
            if this_child.is_dir():
                found = True
                break
    return found


def process_terminal_token_end_node(symbol_name: str) -> None:
    """
    We are at the terminal end of a "AST"; process end-node.
    :param symbol_name: group name
    :ptype symbol_name: str
    :rtype: None
    """
    #    print("  File: %s" % entry.name)
    #    print("  Stack: %s" % [p.name for p in stack])  # Debug: show full stack
    output_vimscript_comment("End-node Terminal Symbol Name (file): %s" % symbol_name)



def output_vimscript_highlight(symbol_name: str, highlight_link_label: str) -> None:
    """
    Generate a Vimscript highlight command
    :param symbol_name: The group name to be highlighted
    :param highlight_link_label:
    :rtype: None
    """
    global target_file_format

    group_name = target_file_format.rstrip('_') + 'HL_' + highlight_link_label
    # iterate and collect name of next keywords
    print("highlight link %s %s" % (symbol_name, group_name))
    # print("highlight link %s %s" % (group_name, highlight_link_label))
    # track all highlight group names for later output
    target_highlights_found.add((group_name, highlight_link_label, symbol_name))


def output_vimscript_syn_match(stack: Deque[Path], path: Path, group_name: str, node_options: Dict[str, Any], non_terminal: bool) -> None:
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
            option_pattern: str = node_options['pattern']
            regex_pattern = option_pattern
            regex_pattern = regex_pattern.rstrip('\'').lstrip('\'')
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
    if is_root_node(stack):
        print("syntax match %s '%s'" % (group_name, pattern))
    else:
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


from typing import Dict, Any

def output_vimscript_nextgroup_error_handlers(error_options: Dict[str, Any]) -> None:
    """

    :param error_options:
    :rtype: None
    """
    global target_symbol_prefix
    
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

    if 'equal' in list_of_foto:
        list_of_foto.remove('equal')
        add_on_pattern = '='
        new_error_group_name = target_symbol_prefix + 'Error_equal_not_found'
        print('\\    %s' % new_error_group_name)
        final_antipattern = r'\v[^' + add_on_pattern + ']'
        target_error_defined.append((new_error_group_name, add_on_pattern, final_antipattern))
        #print('error_defined (running): ', errors_defined)
    # TODO: construct unique error handler
    if not not list_of_foto:
        print('" WARNING: remaining unprogrammed follow_on_to_only options: ', list_of_foto)


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
    output_vimscript_comment(str(path))
    if 'highlight_color_name' in node_options:
        output_vimscript_highlight(symbol_name, node_options['highlight_color_name'])

    # There is a loop here for multiple patterns using exact same group name
    output_vimscript_syn_match(stack, path, symbol_name, node_options, non_terminal=True)
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
    output_vimscript_comment(str(path))
    if 'highlight_color_name' in node_options:
        output_vimscript_highlight(symbol_name, node_options['highlight_color_name'])
    output_vimscript_syn_match(stack, path, symbol_name, node_options, non_terminal=False)
    output_vimscript_comment('')


def start_directory_traverse(start_dirpath: Path, hidden_prefix: str, prefix: str = 'nft_') -> None:
    """

    :return: None
    :param start_dirpath:
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
                if entry.name.startswith(hidden_prefix):
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
                    raise NotADirectoryError('Not sure what to do with this file', entry, ": try cd into directory containing 'syntax-tree'")  # not sure
                    full_symbol_name = construct_symbol_name.get_file(stack, path.name, prefix)
                    process_terminal_token_end_node(full_symbol_name)

        except PermissionError:
            print("  Permission denied: %s" % path.name)
        stack.pop()

    # Run start_directory_traverse() with pathspec to its top-level directory
    start_path = start_dirpath.resolve()  # Convert to Path and resolve
    if start_path.is_file():
        print("Path %s is a file, not a directory; aborted." % start_path.name)
        return
    if not start_path.is_dir():
        print("Path %s is not a directory; aborted." % start_path.name)
        return

    traverse_recursively(start_path)
    # last node traversed here, what's next?


import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Process input and output files.')
    parser.add_argument('-f', '--file-type', metavar='filetype', type=str, required=True, help='Type of file format')
    parser.add_argument('-b', '--base-path', metavar='one-syntax_dir_spec', type=Path, required=False, default=CORPUS_SYNTAX_TREE_DIRPATH, help='Base directory path (default is $CWD)')
    parser.add_argument('-c', '--corpus', metavar='corpus_dir_spec', type=Path, required=False, help='Directory to corpus of syntax tree')
    parser.add_argument('-t', '--template', metavar='template_dir_spec', type=Path, required=False, help='Template file path')
    parser.add_argument('-o', '--output', metavar='output_dir_spec', type=Path, required=False, help='Output file path')
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help='Verbosity level')
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s 1.0.0',
        help="Show program's version number and exit."
    )
    return parser.parse_args()

def main() -> None:
    """
    :return: None
    """
    global target_symbol_prefix
    global target_file_format

    target_symbol_prefix = ''
    args = parse_args()
    if args.file_type is None:
        raise ArgumentTypeError("--file-type argument must be defined")
    else:
        target_file_format = args.file_type

    # Basic directory tree
    # $CWD are not to be changed and expected to be in 'one-syntax' subdirectroy by default, otherwise use '-b' option
    base_dirpath = Path.cwd()
    template_dirpath_relative = Path('templates')  # option '-t'
    corpus_dirpath_relative = Path('corpus')    # option '-c'
    output_dirpath_relative = Path('output')    # option '-o'

    # Obtain user-supplied basepath (either in relative/absolute path)
    if args.base_path:
        base_dirpath = args.base_path

    # Now, merge the base_dirpath (or its other arguments) with the tree
    # Update any syntax corpus dirpath
    if args.corpus:
        # Replace canned syntax tree with user-defined ones
        corpus_dirpath = args.corpus
    else:
        corpus_dirpath = corpus_dirpath_relative
    if not corpus_dirpath.is_dir():
        raise ArgumentTypeError('Corpus \'' + str(corpus_dirpath) + '\' is not a subdirectory')

    if args.template:
        template_dirpath = args.template
    else:
        template_dirpath = template_dirpath_relative
    if not template_dirpath.is_dir():
        raise ArgumentTypeError('Template \'' + str(template_dirpath) + '\' is not a subdirectory')

    if args.output:
        output_dirpath = args.output
    else:
        output_dirpath = output_dirpath_relative
    if not output_dirpath.is_dir():
        raise ArgumentTypeError('Output \'' + str(output_dirpath) + '\' is not a subdirectory')

    # Map out remaining tree pathways (noticed no '_relative' nor absolute notation)
    corpus_fileformat_dirpath = corpus_dirpath / Path(target_file_format)
    corpus_fileformat_tree_dirpath = corpus_fileformat_dirpath / 'syntax-tree'
    corpus_fileformat_platform_dirpath = corpus_fileformat_dirpath / TARGET_EDITOR_PLATFORM

    template_platform_dirpath = template_dirpath / TARGET_EDITOR_PLATFORM

    output_fileformat_dirpath = output_dirpath / Path(target_file_format)
    output_fileformat_platform_dirpath = output_fileformat_dirpath / Path(TARGET_EDITOR_PLATFORM)
    output_vim_syntax_dirpath = output_fileformat_platform_dirpath / 'syntax'
    vim_syntax_subdir = output_vim_syntax_dirpath

    # set our first global options
    options = parse_simple_ini.get_main_options(corpus_fileformat_tree_dirpath)
    opt_prefix: (str|None) = options.get('symbol_name_prefix')
    if opt_prefix is None:
        raise ValueError(f"Missing required main option 'symbol_name_prefix' in {corpus_fileformat_tree_dirpath}/.config.main.ini config file.")
    else:
        target_symbol_prefix = opt_prefix
    target_file_format = target_symbol_prefix.rstrip('_')

    # Your code here
    print(f"File-format: {target_file_format}")
    print(f"Base: {base_dirpath}")
    print(f"Corpus syntax tree: {corpus_fileformat_tree_dirpath}")
    print(f"Build area: {vim_syntax_subdir}")
    print(f"  derived from: {template_platform_dirpath}")
    print(f"  derived from: {corpus_fileformat_platform_dirpath}")
    # Retrieve options from root 'syntax-tree/.config.main.ini

    output_vimscript_comment('AUTO-GENERATED BY YOURS TRULY!')
    # Need to declare highlight firstly before anything
    output_vimscript_highlight_defaults(corpus_fileformat_tree_dirpath)

    # Do top-level differently than rest of tree-traversing
    start_directory_traverse(corpus_fileformat_tree_dirpath, target_symbol_prefix)

    output_error_labels_defined()

if __name__ == '__main__':
    main()


