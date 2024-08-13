import os
import shutil
import sys
import argparse
from datetime import datetime

# Simulate command-line arguments for Spyder IDE
# This block is only for development in Spyder to simulate command-line input
if 'spyder' in sys.modules:
    sys.argv = ['file_manager.py', '-m', 'basic', '-d', '/Users/harrisonryan/Downloads']

def parse_arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='File Manager Script')
    parser.add_argument('-m', required=True, choices=['basic', 'elevated', 'admin'], 
                        help='Mode of operation: basic, elevated, or admin.')
    parser.add_argument('-d', help='Directory path to start browsing. Optional; if not provided, defaults to the current working directory.')
    return parser.parse_args()

def setup_logging():
    """
    Set up the logging directory and file.

    Creates a directory named 'Python_Log' in the user's home directory if it does not exist.
    Returns:
        str: Path to the log file.
    """
    home_dir = os.path.expanduser('~')  # Get the path to the user's home directory
    log_dir = os.path.join(home_dir, 'Python_Log')  # Define the log directory path
    if not os.path.exists(log_dir):  # Check if the directory does not exist
        os.makedirs(log_dir)  # Create the directory if it does not exist
    log_file = os.path.join(log_dir, 'system_log.txt')  # Define the path for the log file
    return log_file

def log_action(action, log_file):
    """
    Log an action to the specified log file.

    Args:
        action (str): Description of the action to log.
        log_file (str): Path to the log file.
    """
    with open(log_file, 'a') as f:  # Open the log file in append mode
        f.write(f"{datetime.now()}: {action}\n")  # Write the action with a timestamp

def list_directory(path):
    """
    List files and directories in the specified path.

    Args:
        path (str): The directory path to list contents from.
    """
    try:
        entries = os.listdir(path)  # List all entries in the directory
        for entry in entries:
            entry_path = os.path.join(path, entry)  # Get the full path of the entry
            if os.path.isdir(entry_path):  # Check if it is a directory
                print(f"{entry}/")  # Print the directory name with a trailing slash
            else:
                size = os.path.getsize(entry_path)  # Get the size of the file
                print(f"{entry} - {size} bytes")  # Print the file name and size
    except Exception as e:
        print(f"Error listing directory: {e}")  # Print an error message if listing fails

def change_directory(current_path):
    """
    Change the current directory to a new path.

    Prompts the user to enter a new directory path and updates `current_path` if the new path is valid.
    
    Args:
        current_path (str): The current directory path.

    Returns:
        str: The updated directory path if valid, otherwise the original path.
    """
    new_path = input("Enter the new directory path: ")  # Prompt user for a new directory path
    if not os.path.isdir(new_path):  # Check if the new path is a valid directory
        print("Invalid directory.")  # Print an error message if invalid
    else:
        current_path = new_path  # Update the current path to the new path
    return current_path

def copy_item(source, destination):
    """
    Copy a file or directory from source to destination.

    Args:
        source (str): The path to the source file or directory.
        destination (str): The path to the destination location.
    """
    try:
        if os.path.isdir(source):  # Check if the source is a directory
            shutil.copytree(source, destination)  # Copy the directory and its contents
            print(f"{os.path.basename(source)} was copied to {destination}")  # Notify user of the copy operation
        else:
            shutil.copy(source, destination)  # Copy a single file
            print(f"{os.path.basename(source)} was copied to {destination}")  # Notify user of the copy operation
    except Exception as e:
        print(f"Error copying item: {e}")  # Print an error message if copy fails

def move_item(source, destination):
    """
    Move a file or directory from source to destination.

    Args:
        source (str): The path to the source file or directory.
        destination (str): The path to the destination location.
    """
    try:
        shutil.move(source, destination)  # Move the file or directory to the new location
        print(f"{os.path.basename(source)} was moved to {destination}")  # Notify user of the move operation
    except Exception as e:
        print(f"Error moving item: {e}")  # Print an error message if move fails

def delete_item(item_path, backup_dir):
    """
    Delete a file or directory after backing it up.

    Args:
        item_path (str): The path to the file or directory to delete.
        backup_dir (str): The path to the backup directory where deleted items will be copied.
    """
    try:
        if not os.path.exists(backup_dir):  # Check if the backup directory exists
            os.makedirs(backup_dir)  # Create the backup directory if it does not exist
        item_name = os.path.basename(item_path)  # Get the base name of the item to delete
        backup_path = os.path.join(backup_dir, f"deleted_{item_name}")  # Define the backup path with 'deleted_' prefix
        if os.path.isdir(item_path):  # Check if the item is a directory
            shutil.copytree(item_path, backup_path)  # Copy the entire directory to backup
        else:
            shutil.copy(item_path, backup_path)  # Copy the file to backup
        if os.path.isdir(item_path):  # If it is a directory, remove it
            shutil.rmtree(item_path)  # Remove the directory and its contents
        else:
            os.remove(item_path)  # Remove the file
        print(f"{item_name} was deleted and backed up.")  # Notify user of the delete operation
    except Exception as e:
        print(f"Error deleting item: {e}")  # Print an error message if delete fails

def main():
    """
    Main function to handle user inputs and operations.

    This function parses command-line arguments, sets up logging, and provides a menu-driven interface 
    for file and directory operations based on the selected mode (basic, elevated, admin).
    """
    args = parse_arguments()  # Parse command-line arguments
    log_file = setup_logging()  # Set up the log file
    current_dir = args.d if args.d else '/Users/harrisonryan/Downloads'  # Set the current directory based on arguments or default

    # Validate that the current directory path is absolute and does not contain '..'
    if not os.path.isabs(current_dir) or '..' in os.path.relpath(current_dir, '/Users/harrisonryan'):
        print("Invalid directory path.")  # Print error message for invalid path
        sys.exit(1)  # Exit the program with an error code

    while True:
        # Display menu options based on the mode
        print("\nMenu:")
        print("1. List directory")  # Basic functionality
        if args.m in ['elevated', 'admin']:
            print("2. Copy item")  # Additional functionality for elevated and admin modes
        if args.m == 'admin':
            print("3. Move item")  # Additional functionality for admin mode
            print("4. Delete item")  # Additional functionality for admin mode
        print("0. Exit")  # Option to exit the program

        choice = input("Select an option: ")  # Get user choice from menu

        if choice == '0':
            break  # Exit the loop and terminate the program
        elif choice == '1':
            list_directory(current_dir)  # List contents of the current directory
        elif choice == '2' and args.m in ['elevated', 'admin']:
            source = input("Enter source path: ")  # Prompt user for source path
            destination = input("Enter destination path: ")  # Prompt user for destination path
            if os.path.exists(source):  # Check if the source exists
                copy_item(source, destination)  # Perform copy operation
                log_action(f"Copied {source} to {destination}", log_file)  # Log the action
            else:
                print("Source does not exist.")  # Print error message for non-existent source
        elif choice == '3' and args.m == 'admin':
            source = input("Enter source path: ")  # Prompt user for source path
            destination = input("Enter destination path: ")  # Prompt user for destination path
            if os.path.exists(source):  # Check if the source exists
                move_item(source, destination)  # Perform move operation
                log_action(f"Moved {source} to {destination}", log_file)  # Log the action
            else:
                print("Source does not exist.")  # Print error message for non-existent source
        elif choice == '4' and args.m == 'admin':
            item_path = input("Enter path of item to delete: ")  # Prompt user for the path of the item to delete
            backup_dir = os.path.join(os.path.expanduser('~'), 'backups')  # Define backup directory path
            if not os.path.exists(backup_dir):  # Check if the backup directory exists
                os.makedirs(backup_dir)  # Create the backup directory if it does not exist
            if os.path.exists(item_path):  # Check if the item to delete exists
                delete_item(item_path, backup_dir)  # Perform delete operation
                log_action(f"Deleted {item_path}", log_file)  # Log the action
            else:
                print("Item does not exist.")  # Print error message for non-existent item
        else:
            print("Invalid choice.")  # Print error message for invalid menu choice

if __name__ == "__main__":
    main()
