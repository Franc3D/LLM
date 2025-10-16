import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):

    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if absolute_working_directory not in absolute_path:
        return f"Error: Cannot execute {file_path} as it is outside the permitted working directory"
    if not os.path.isfile(absolute_path):
        return f"Error: File {file_path} not found."
    if not os.path.splitext(absolute_path)[1] == ".py":
        return f"Error: {file_path} is not a Python file."
    
    try:
        completed_process = subprocess.run(["python3", absolute_path] + args, timeout=30, capture_output=True, cwd=absolute_working_directory)
        
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout is None and completed_process.stderr is None:
            return "No output produced."
        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"