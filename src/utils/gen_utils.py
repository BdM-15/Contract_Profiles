#General reusable functions
import os, glob
from docx.shared import Pt, RGBColor

# This function finds the latest file in a folder based on the file pattern.  It will determine if the file is .xlsx or .csv and read the file accordingly.
def find_latest_file(folder_path: str, file_pattern: str) -> str:
    """
    Find the latest file in a folder based on the file pattern.

    Args:
    folder_path (str): The path to the folder where the files are located.
    file_pattern (str): The pattern to search for the latest file.

    Returns:
    str: The path to the latest file found in the folder.
    """
   
    file_list = glob.glob(os.path.join(folder_path, file_pattern))

    if file_list:
        latest_file = max(file_list, key=os.path.getctime)
        # Print the latest file to the console for confirmation
        # print(f"Latest file: {latest_file}") 
        return latest_file # Return the path to the latest file
    else:
        raise FileNotFoundError(f"No file matching the pattern {file_pattern} found in {folder_path}.")
    
#This function will identify any older files than the most recent file in the raw data folder and move them to the archive folder.  If an archive folder does not exist, it will create one.
def archive_folder_files(current_folder: str, file_list: list, latest_file: str) -> None:
    """
    Move older files in the raw data folder to the archive folder.

    Args:
    current_folder (str): The path to the data folder we want to have an archive.
    file_list (list): A list of files in the data folder to determine if any older files exist.
    latest_file (str): The path to the latest file in the data folder.

    Returns:
    None
    """
    archive_folder = os.path.join(current_folder, 'archive') # Define the archive folder location

    #  Create the archive folder if it does not exist
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)
    for file in file_list: # Loop through the files in the raw data folder
        if file != latest_file: # Check if the file is not the latest file
            os.rename(file, os.path.join(archive_folder, os.path.basename(file))) # Move the older files to the archive folder

def remove_old_files(folder_path: str, file_pattern: str) -> None:
    """
    Check for the latest file in the folder and remove older files in a folder based on the file pattern.

    Args:
    folder_path (str): The path to the folder where the files are located.
    file_pattern (str): The pattern to search for the files to remove.

    Returns:
    None
    """
    # Find the latest file in the folder based on the file pattern and define it as the latest_file_to_keep
    latest_file_to_keep = find_latest_file(folder_path, file_pattern)
    
    # Check for any folders older than the latest file and remove them
    for file in glob.glob(os.path.join(folder_path, file_pattern)):
        if file != latest_file_to_keep:
            os.remove(file)
            
def does_folder_exist(folder_path: str) -> None:
    """
    Check if a folder exists and create it if it does not.

    Args:
    folder_path (str): The path to the folder to check.

    Returns:
    bool: True if the folder exists, False otherwise.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def does_file_exist(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
    file_path (str): The path to the file to check.

    Returns:
    bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)
    
def get_file_pattern(file_path: str) -> str:
    """
    Get the file pattern from a file path.

    Args:
    file_path (str): The path to the file.

    Returns:
    str: The file pattern extracted from the file path.
    """
    return os.path.basename(file_path)

def get_file_name(file_path: str) -> str:
    """
    Get the file name from a file path.

    Args:
    file_path (str): The path to the file.

    Returns:
    str: The file name extracted from the file path.
    """
    return os.path.splitext(os.path.basename(file_path))[0]

# This helper function to change the font size of the non-header cells to size 9 Calibri.
def set_cell_font(cell, font_name='Calibri', font_size=9, bold=False, color=None):
    """
    Set the font for a table cell.
    """
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.bold = bold
            if color:
                run.font.color.rgb = RGBColor(*color)