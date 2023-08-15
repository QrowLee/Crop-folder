import os
import pdf2image
import subprocess

path = "D:/Calibre Library/Ron Mars/swampgod issue3 (2605)/swampgod issue3 - Ron Mars.pdf"
output_path = path.replace(".pdf", ".cbz")

# Convert PDF to images
pages = pdf2image.convert_from_path(path)

# Save images as JPEG
for i, page in enumerate(pages):
    page.save('page' + str(i) + '.jpg', 'JPEG')

# Create a list of image files
image_files = ['page' + str(i) + '.jpg' for i in range(len(pages))]

import zipfile

def compress_to_zip(source_files, output_path):
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for file in source_files:
            zipf.write(file)

# Specify the source files to compress
source_files = image_files

# Compress the files to a zip archive
compress_to_zip(source_files, output_path)

# Clean up temporary image files
for file in image_files:
    os.remove(file)
