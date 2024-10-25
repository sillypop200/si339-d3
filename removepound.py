import os

# Define the folder path
meets_folder = 'meets'

# Ensure the folder exists
if not os.path.exists(meets_folder):
    print(f"The folder '{meets_folder}' does not exist.")
else:
    # Walk through the folder
    for root, dirs, files in os.walk(meets_folder):
        for file in files:
            if '#' in file:
                # Create the current full path to the file
                old_file_path = os.path.join(root, file)
                # Create the new file name by removing '#' symbol
                new_file_name = file.replace('#', '')
                # Create the new full path to the file
                new_file_path = os.path.join(root, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")

    print("File renaming completed.")