import os
from typing import List


def find_pdf_files(path: str) -> List[str]:
    """
    Searches the specified directory for all files with the .pdf extension.

    This function uses os.listdir() to list all entries in the directory
    and filters the list to include only those ending with '.pdf'.

    Args:
        path: The path to the directory to search (e.g., 'C:/Documents/Reports' or './data').

    Returns:
        A list of strings, where each string is the full filename of a
        PDF file found in the directory.

    Raises:
        FileNotFoundError: If the provided path does not exist.
        NotADirectoryError: If the provided path exists but is not a directory.
    """

    # 1. Input Validation: Check if the path exists and is a directory
    if not os.path.exists(path):
        raise FileNotFoundError(f"Error: The path '{path}' does not exist.")
    if not os.path.isdir(path):
        raise NotADirectoryError(
            f"Error: The path '{path}' is not a directory."
        )

    # 2. List all files and directories in the given path
    try:
        entries = os.listdir(path)
    except PermissionError:
        print(f"Warning: Permission denied when accessing '{path}'. Skipping.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while listing files: {e}")
        return []

    pdf_files = []

    # 3. Iterate through the entries and check for the '.pdf' extension
    for entry in entries:
        # Check if the entry is a file (not a subdirectory) and ends with '.pdf'
        # Note: os.path.join creates the full path for the check
        full_path = os.path.join(path, entry)

        # We check if it's a file first to avoid issues with subdirectories
        # that might coincidentally end in '.pdf' (though unlikely)
        if os.path.isfile(full_path) and entry.lower().endswith(".pdf"):
            pdf_files.append(entry)

    return pdf_files


if __name__ == "__main__":
    print(find_pdf_files("output/"))
