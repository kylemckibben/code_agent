import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_working_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir

        print(f'Results for {"current" if directory == "." else f"'{directory}'"} directory:')

        if not valid_working_dir:
            return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'\tError: "{directory}" is not a directory'

        dir_contents = []
        for item in os.listdir(target_dir):
            file_size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))
            item_str = f'- {item}: file_size={file_size}, is_dir={is_dir}' 
            dir_contents.append(item_str)

        return "\n".join(dir_contents)
    except Exception as e:
        return f'\tError: {e}'

