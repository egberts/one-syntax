"""
File: construct_symbol_name.py
"""

"""
File: construct_symbol_name.py
Purpose: Construct consistent symbol/group names from a parsing stack.
"""

import re
import logging
import pathlib
from typing import List, Deque

logging.basicConfig(level=logging.ERROR)

def convert(previous_name: str, name: str) -> str:
    """

    :param previous_name: The previous file name to use for context
    :type previous_name: `str`
    :param name:  The file name to convert before passing off as a symbol name
    :type name: `str`
    :return: The converted name
    :rtype: `str`
    """
    if len(name) == 1:
        if name == '{':
            return previous_name.lower() + '_block'
        if name == '=':
            return 'equal'
        if name == '#':
            return 'hash'
        if name == '[':
            # noinspection SpellCheckingInspection
            return 'lbracket'
        if name == ']':
            # noinspection SpellCheckingInspection
            return 'rbracket'
    return name


# noinspection PyUnresolvedReferences
def get_dir_stackless(syntax_root_path: pathlib.Path, file_path: pathlib.Path) -> str:
    """
    Convert a file path to a valid Python snake_case variable name.
    Iterates through each path component, applying special conversions if provided.

    :param syntax_root_path: The root path to remove from the start (e.g., '/path/to').
    :type syntax_root_path: `Path`
    :param file_path: The file path to convert (e.g., '/path/to/sub_dir/config.ini').
    :type file_path: `Path`
    :return: A constructed symbol name string.
    :rtype: `str`
    :raises ValueError: If the stack is invalid (e.g., starts with '{').

    Returns:
        A valid snake_case variable name.
    """
    # Sample path and special conversions
    special_conversions: dict[str, str] = {
        "sub-dir": "subdir",  # Replace 'sub-dir' with 'subdir'
        "config.ini": "config"  # Replace 'config.ini' with 'config'
    }
    # Convert to Path object and get all parts (excluding root '/')
    # Remove top n directories ("corpus/ini/syntax-tree")
    # Remove root path
    try:
        relative_path = file_path.relative_to(syntax_root_path)
    except ValueError:
        relative_path = file_path  # Fallback if path is not under root
    print(f'parts: {file_path.parts}')
    parts = list(relative_path.parts)[1:] if relative_path.is_absolute() else relative_path.parts

    # Process each part
    valid_parts: List[str] = []
    parent_part = ''
    for part in parts:
        # Apply special conversion if exists
        part = special_conversions.get(part, part)

        # Remove invalid characters, replace with underscore
        part = re.sub(r'[^a-zA-Z0-9]', '_', part)
        # Convert to lowercase and remove leading/trailing underscores
        part = part.lower().strip('_')
        # Skip empty parts (e.g., from consecutive underscores)
        converted_part = part
        if part:
            converted_part = convert(parent_part, part)
            # Preserve all-uppercase names (TABLE, CHAIN, etc.)
            if not converted_part.isupper():
                # Normalize to snake_case: lowercased, non-alphanumerics → underscores
                converted_part = re.sub(r'[^a-zA-Z0-9]+', '_', converted_part.lower()).strip('_')
            valid_parts.append(converted_part)
        parent_part = converted_part

    # Join parts with underscores
    variable_name = '_'.join(valid_parts)

    # Ensure the name is a valid Python identifier
    if not variable_name or not variable_name.isidentifier():
        return 'invalid_path_name'

    # Ensure it doesn't start with a digit
    if variable_name[0].isdigit():
        variable_name = f"path_{variable_name}"

    return variable_name


def get_dir(stack: Deque[pathlib.Path], prefix: str) -> str:
    """
    Construct a snake_case symbol/group name string from a parsing stack.

    :param stack: A sequence of parsed tokens/nodes (each must have a `.name` attribute).
    :type stack: `Deque[pathlib.Path]`
    :param prefix: A string prefix (e.g., 'nft_' for Vimscript group names).
    :type stack: `str`
    :return: A constructed symbol name string.
    :rtype: `str`
    :raises ValueError: If the stack is invalid (e.g., starts with '{').
    """
    # If too short, a simple quit with an empty string shall suffice
    #if len(stack) <= 1:  # i think this is no longer needed now that root node has its own traversal function
    #    return ''
    names: List[str] = []
    parent_name = ''

    for item in list(stack)[1:]:
        name = getattr(item, "name", None)
        if not name:
            raise ValueError("Stack item missing 'name' attribute")
        if len(name) == 0:
            raise ValueError("Empty name!")

        converted_name = convert(parent_name, name)
        if name.isupper():
            # Preserve all-uppercase names (TABLE, CHAIN, etc.)
            snake_case_name = converted_name
        else:
            # Normalize to snake_case: lowercased, non-alphanumerics → underscores
            snake_case_name = re.sub(r'[^a-zA-Z0-9]+', '_', converted_name.lower()).strip('_')

        names.append(snake_case_name)
        parent_name = snake_case_name

    # Safely join prefix and names (avoid duplicate underscores)
    if len(names) == 0:
        list_of_syms = ''
    else:
        list_of_syms = '_' + '_'.join(names)

    # Safely join prefix and names (avoid duplicate underscores)
    return prefix.rstrip('_') + list_of_syms


def get_file(stack: Deque[pathlib.Path], filename2: str, prefix: str) -> str:
    """
    Construct a snake_case symbol/group name string from a parsing stack.

    :param stack: A sequence of parsed tokens/nodes (each must have a `.name` attribute).
    :type stack: `Deque[pathlib.Path]`
    :param filename2: A string suffix (e.g., 'config' for Vimscript variable names).
    :type filename2: `str`
    :param prefix: A string prefix (e.g., 'nft_' for Vimscript group names).
    :type prefix: `str`
    :return: A constructed symbol name string.
    :rtype: `str`
    :raises ValueError: If the stack is invalid (e.g., starts with '{').
    """
    # If too short, a simple quit with an empty string shall suffice
    #if len(stack) <= 1:  # i think this is no longer needed now that root node has its own traversal function
    #    return ''

    parent_name = ''
    names: List[str] = []

    # Process each part
    for item in list(stack)[1:]:
        # Extract name attribute
        name = getattr(item, "name", None)
        # Validate name
        if not name:
            raise ValueError("Stack item missing 'name' attribute")
        if len(name) == 0:
            raise ValueError("Empty name!")

        # Apply special conversion if exists
        converted_name = convert(parent_name, name)
        if name.isupper():
            # Preserve all-uppercase names (TABLE, CHAIN, etc.)
            snake_case_name = '_' + converted_name
        else:
            # Normalize to snake_case: lowercased, non-alphanumerics → underscores
            snake_case_name = re.sub(r'[^a-zA-Z0-9]+', '_', converted_name.lower()).strip('_')

        # Append to names list
        names.append(snake_case_name)

        # Update parent_name for next iteration
        parent_name = snake_case_name

    # Safely join prefix and names (avoid duplicate underscores)
    if len(names) == 0:
        list_of_syms = ''
    else:
        list_of_syms = '_' + '_'.join(names)

    # Safely join prefix and names (avoid duplicate underscores)
    return prefix.rstrip('_') + list_of_syms + '_' + filename2
