import os

def get_lines(f_handle, lines):
    """  """
    return [line for index, line in enumerate(f_handle) if index in lines]

def file_not_found_msg(filename):
    return f"File '{filename}' not found! Please check the filename and file directory."

def convert_file_ext_to_json(filename):
        """ Strips extension e.g. '.txt' from the filename and appends '.json' """
        return os.path.splitext(filename)[0] + '.json'

