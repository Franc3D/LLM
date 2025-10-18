import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))
    
    
    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return "Error: Cannot list {} as it is outside the permitted working directory".format(directory)
    #if the directory does not exist, return an error
    if not os.path.isdir(absolute_path):
        return f"Error: {directory} is not a directory"

    try:
        file_names = os.listdir(absolute_path)
        data_list = []
        for name in file_names:
            file_size = os.path.getsize(os.path.join(absolute_path, name))
            is_file = os.path.isfile(os.path.join(absolute_path, name))
            data = f"- {name}: file_size={file_size} bytes, is_dir={not is_file}"
            data_list.append(data)
        return "\n".join(data_list)
    except Exception as e: 
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "gets the content of a file up to 10000 chars, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file, relative to the working directory. If not provided, lists files in the working directory itself."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "execute a .py file possibly using args, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="A list of args to use when running the python file, either a full string or separate words works"
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "replace the content of a file with the content argument, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that we want to write inside the file"
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
