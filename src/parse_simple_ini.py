"""
Configuration file and its settings
"""
import pathlib
from typing import Dict


def read(file_path: pathlib.Path) -> Dict[str, str]:
    """
    Reads a simple INI-style configuration file and returns its contents as a dictionary.

    :param file_path: Path to the configuration file.
    :type file_path: `pathlib.Path`
    :return: Dictionary containing key-value pairs from the file.
    :rtypeL: `Dict[str, str]`
    :raises FileNotFoundError: If the specified file does not exist.
    """
    config: Dict[str, str] = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(('#', ';')):
                    continue  # Skip malformed lines (lines without '=' separating key and value)
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    return config


valid_main_options = {
    'symbol_name_prefix'
}

valid_node_options = {
    'pattern',
    'highlight_color_name',
    'squishable_with_next_token',
    'follow_on_to_only',
    'must_follow_lines_to_end_region_delimiter',
}

valid_node_follow_on_options = {
    'new_line',  # \n
    'end_of_statement',  # ;
    'start_block_delimiter',  # {
    'end_block_delimiter',  # }
    'equal',  # =
    'start_parenthesis',  # (
    'end_parenthesis',  # )
    'slash',  # /
    'at_symbol',  # @
    'dot',  # .
    'colon',  # :
    'comma',  #
    'plus',  # +
    'dash',  # -
    'asterisk',  # *
    'hashmark',  # #
}


def get_main_options(path: pathlib.Path) -> Dict[str, str]:
    """
    Reads main options from a configuration file, validates them, and returns a dictionary of options.
    :param path: Path to the directory containing the configuration file.
    :type path: `pathlib.Path`
    :return: Dictionary of main options.
    :rtype: `Dict[str, str]`
    :raises ValueError: If an invalid option is found.
    """
    # Check path exists and is a directory
    main_config_filespec = path / '.config.main.ini'
    # If no main config file, return empty dictionary
    if not main_config_filespec.exists():
        return {}
    # Read config file
    retrieved_main_options = read(main_config_filespec)
    # enforce valid options in main config file.
    for this_main_option in retrieved_main_options:
        # Validate option name
        if this_main_option not in valid_main_options:
            raise ValueError(f"Invalid main option '{this_main_option}' in config {main_config_filespec} file.")
    return retrieved_main_options


def get_node_options(path: pathlib.Path) -> Dict[str, str]:
    """
    Reads node options from a configuration file, validates them, and returns a dictionary of options.

    :param path: Path to the directory containing the configuration file.
    :type path: `pathlib.Path`
    :return: Dictionary of node options.
    :rtype: `Dict[str, str]`
    :raises ValueError: If an invalid option or follow-on token is found.
    """
    # Check path exists and is a directory
    if not path.exists():
        raise FileNotFoundError(f"Path '{path}' does not exist.")
    if not path.is_dir():
        raise NotADirectoryError(f"Path '{path}' is not a directory.")
    # Check for .config.ini file in directory
    node_config_path = path / '.config.ini'
    if not node_config_path.exists():
        # No config file, return empty dictionary
        return {}
    # Read config file
    retrieved_node_config_options = read(node_config_path)
    # enforce valid options in syntax tree's config.ini file.
    for this_node_option in retrieved_node_config_options:
        # Validate option name
        if this_node_option not in valid_node_options:
            raise ValueError(f"Invalid option '{this_node_option}' in config {node_config_path} file.")
        # Validate follow-on tokens if present
        if this_node_option == 'follow_on_to_only' and retrieved_node_config_options['follow_on_to_only']:
            tokens = retrieved_node_config_options['follow_on_to_only'].split(',')
            # Validate further
            for token in tokens:
                # Strip whitespace
                token = token.strip()
                # Validate token
                if token not in valid_node_follow_on_options:
                    raise ValueError(
                        f"Invalid follow-on token '{token}' in config {node_config_path} file. "
                        f"Valid tokens are: {valid_node_follow_on_options}"
                    )
    return retrieved_node_config_options
