import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_working_dir = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir

        if not valid_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if abs_file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(
                command, 
                cwd=abs_working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
        output_str = ""
        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout == "" and completed_process.stderr == "":
            output_str += "No output produced"
        if completed_process.stdout != "":
            output_str += f'STDOUT: {completed_process.stdout}\n'
        if completed_process.stderr != "":
            output_str += f'STDERR: {completed_process.stderr}\n' 
        return output_str
    except Exception as e:
        return f'Error: executing Python file: {e}'

