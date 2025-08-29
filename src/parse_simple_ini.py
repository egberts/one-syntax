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
    'follow_lines_to_end_region_delimiter',
    'skip_all_following_whitespace',
    'skip_any_new_line',
    'skip_all_empty_lines'
}


def get_main_options(path: pathlib):
    """

    :param path:
    """
    main_config_filespec = path / 'config.main.ini'
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
    node_config_filespec = path / 'config.ini'
    if not node_config_filespec.exists():
        return {}
    retrieved_node_config_options = read(node_config_filespec)
    # validate options
    for this_node_option in retrieved_node_config_options:
        if this_node_option not in valid_node_options:
            raise ValueError(f"Invalid option '{this_node_option}' in config {node_config_filespec} file.")
    return retrieved_node_config_options
