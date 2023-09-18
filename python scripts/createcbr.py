import os
from rarfile import RarFile

def create_cbr_from_folder(folder_path, output_filename):
    # Get a list of all JPG files in the folder
    jpg_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.jpg')]

    # Create a RAR archive with maximum compression
    with RarFile(output_filename, 'w', compress='store') as archive:
        for jpg_file in jpg_files:
            file_path = os.path.join(folder_path, jpg_file)
            archive.write(file_path, os.path.basename(file_path))

if __name__ == "__main__":
    input_folder = "path/to/your/input/folder"
    output_filename = "output.cbr"

    create_cbr_from_folder(input_folder, output_filename)
    print(f"CBR file '{output_filename}' created successfully.")
