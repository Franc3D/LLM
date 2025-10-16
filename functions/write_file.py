import os

def write_file(working_directory, file_path, content):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if absolute_working_directory not in absolute_path:
        return f"Error: cannot write to {file_path} as it is outside the permitted working directory"
    
    try:
        if not os.path.exists(os.path.dirname(absolute_path)): 
            os.makedirs(os.makedirs(os.path.dirname(absolute_path), exist_ok=False))
        
        with open(absolute_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {e}"