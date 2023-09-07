import os
import shutil

# Specify the source directory where the files are located
source_directory = "./response"

# Define the destination directories
destination_directories = {}

# Loop through the files in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith(".txt"):
        # Extract the domain name from the file name
        domain_parts = filename.split(".")

        # Check if the file name has at least four parts (including .txt)
        if len(domain_parts) >= 4:
            domain_name_parts = domain_parts[-4:-1]
            domain_name = ".".join(domain_name_parts)
        else:
            # If the file name doesn't have enough parts, skip the file
            continue

        # Create the destination directory if it doesn't exist
        if domain_name not in destination_directories:
            destination_directory = os.path.join('domain_directory', domain_name)
            os.makedirs(destination_directory, exist_ok=True)
            destination_directories[domain_name] = destination_directory
        else:
            destination_directory = destination_directories[domain_name]

        # Move the file to the destination directory
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(destination_directory, filename)
        shutil.copy(source_path, destination_path)