import os

from constants import CHAR_READ_MAX

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_working_dir = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir

        if not valid_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, "r") as f:
            content = f.read(CHAR_READ_MAX)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {CHAR_READ_MAX} characters]'

        return content
    except Exception as e:
        return f'Error: {e}'
    
