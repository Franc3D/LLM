import os

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
