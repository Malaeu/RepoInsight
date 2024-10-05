import os
from typing import Callable

def get_file_extension(file_path: str) -> str:
    """
    Retrieve the file extension from a file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file extension in lowercase.
    """
    return os.path.splitext(file_path)[1].lower()

def is_text_file(file_path: str) -> bool:
    """
    Determine if a file is a text file based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if it's a text file, False otherwise.
    """
    text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml'}
    return get_file_extension(file_path) in text_extensions

def is_code_file(file_path: str) -> bool:
    """
    Determine if a file is a code file based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if it's a code file, False otherwise.
    """
    code_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.ts'}
    return get_file_extension(file_path) in code_extensions

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes.
    """
    return os.path.getsize(file_path)

# Additional utility functions can be added here as needed.