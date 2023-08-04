def get_current_file_contents(filename: str):
    with open(filename, "r") as file:
        contents = file.read()
    return contents
