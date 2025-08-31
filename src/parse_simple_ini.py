"""
Configuration file and its settings
"""
import pathlib


def read(file_path: pathlib):
    """

    :param file_path:
    :return:
    """
    config = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(('#', ';')):
                    continue
                if '=' not in line:
                    continue  # Skip malformed lines
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
        # print(f"File '{file_path}' not found.")
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
    'new_line',          # \n
    'end_of_statement',  # ;
    'start_block_delimiter',  # {
    'end_block_delimiter',    # }
    'equal',    # =
    'start_parenthesis',    # (
    'end_parenthesis',      # )
    'slash',    # /
    'at_symbol',    # @
    'dot',    # .
    'colon',    # :
    'comma',    # 
    'plus',     # +
    'dash',     # -
    'asterisk',    # *
    'hashmark',    # #
}


def get_main_options(path: pathlib):
    """

    :param path:
    """
    main_config_filespec = path / '.config.main.ini'
    if not main_config_filespec.exists():
        return {}
    retrieved_main_options = read(main_config_filespec)
    # validate options
    for this_main_option in retrieved_main_options:
        if this_main_option not in valid_main_options:
            raise ValueError(f"Invalid main option '{this_main_option}' in config {main_config_filespec} file.")
    return retrieved_main_options


def get_node_options(path: pathlib):
    """

    :param path:
    """
    node_config_filespec = path / '.config.ini'
    if not node_config_filespec.exists():
        return {}
    retrieved_node_config_options = read(node_config_filespec)
    # validate options
    for this_node_option in retrieved_node_config_options:
        if this_node_option not in valid_node_options:
            raise ValueError(f"Invalid option '{this_node_option}' in config {node_config_filespec} file.")

    if 'follow_on_to_only' in retrieved_node_config_options:
        if retrieved_node_config_options['follow_on_to_only']:
            # Validate further
            for this_follow_on in retrieved_node_config_options['follow_on_to_only'].split(","):
                if this_follow_on not in valid_node_follow_on_options:
                    raise ValueError("Invalid follow-on token " + this_follow_on + " in config " + str(node_config_filespec) +" file.")
    return retrieved_node_config_options
