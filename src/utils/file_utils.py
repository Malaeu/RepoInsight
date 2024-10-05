import os

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()

def is_text_file(file_path):
    text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml']
    return get_file_extension(file_path) in text_extensions

def is_code_file(file_path):
    code_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.ts']
    return get_file_extension(file_path) in code_extensions

def get_file_size(file_path):
    return os.path.getsize(file_path)

# Add more utility functions as needed