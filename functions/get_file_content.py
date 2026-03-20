import os

from constants import CHAR_READ_MAX
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return contents of specified file, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read contents from (if it exists), max of 10000 characters will be read", 
            ),
        },
        required=["file_path"],
    ),
)

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
    
