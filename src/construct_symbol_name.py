"""
File: construct_symbol_name.py
"""

"""
File: construct_symbol_name.py
Purpose: Construct consistent symbol/group names from a parsing stack.
"""

import re
import logging
from collections.abc import Sequence
from typing import Any

logging.basicConfig(level=logging.ERROR)

def convert(previous_name: str, name: str) -> str:
    """

    :param previous_name:
    :param name:
    :return:
    """
    if len(name) == 1:
        if name == '{':
            return previous_name.lower() + '_block'
        if name == '=':
            return 'equal'
        if name == '#':
            return 'hash'
    return name


def get_dir(stack: Sequence[Any], prefix: str) -> str:
    """
    Construct a snake_case symbol/group name string from a parsing stack.

    :param stack: A sequence of parsed tokens/nodes (each must have a `.name` attribute).
    :param prefix: A string prefix (e.g., 'nft_' for Vimscript group names).
    :return: A constructed symbol name string.
    :raises ValueError: If the stack is invalid (e.g., starts with '{').
    """
    # If too short, a simple quit with an empty string shall suffice
    #if len(stack) <= 1:  # i think this is no longer needed now that root node has its own traversal function
    #    return ''

    names = []
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


def get_file(stack: Sequence[Any], filename2: str, prefix: str) -> str:
    """
    Construct a snake_case symbol/group name string from a parsing stack.

    :param filename:
    :param stack: A sequence of parsed tokens/nodes (each must have a `.name` attribute).
    :param prefix: A string prefix (e.g., 'nft_' for Vimscript group names).
    :return: A constructed symbol name string.
    :raises ValueError: If the stack is invalid (e.g., starts with '{').
    """
    # If too short, a simple quit with an empty string shall suffice
    #if len(stack) <= 1:  # i think this is no longer needed now that root node has its own traversal function
    #    return ''

    names = []
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
            snake_case_name = '_' + converted_name
        else:
            # Normalize to snake_case: lowercased, non-alphanumerics → underscores
            snake_case_name = re.sub(r'[^a-zA-Z0-9]+', '_', converted_name.lower()).strip('_')

        names.append(snake_case_name)
        parent_name = snake_case_name

    if len(names) == 0:
        list_of_syms = ''
    else:
        list_of_syms = '_' + '_'.join(names)

    # Safely join prefix and names (avoid duplicate underscores)
    return prefix.rstrip('_') + list_of_syms + '_' + filename2