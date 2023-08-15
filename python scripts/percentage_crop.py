
import os
from PIL import Image
import re

# Set the path to the folder containing the images
src_path = "cropinput"
save_path = "cropoutput"
# Set the new dimensions for the cropped image
width_percentage = 0.93
height_percentage = 0.89
shift_right = 0.02
shift_down = 0.000
flip = True

files = os.listdir(src_path)

startFileByName = False
startfile = 4
endfile = 15

pattern = r"\d+"

# Loop through every file in the folder
counter = 0
for counter, filename in enumerate(files, start = startfile):
    
    if (startFileByName) :
        match = re.search(pattern, filename)
        if match:
            counter = int(match.group())

    if (counter < startfile):
        continue
    if (counter > endfile):
        break

    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):

        # Open the original image
        image_path = os.path.join(src_path, filename)
        image_save = os.path.join(save_path, filename)
        image = Image.open(image_path)

        # Get the original size of the image
        width, height = image.size

        # Calculate the new dimensions based on the percentage
        new_width = int(width * width_percentage)
        new_height = int(height * height_percentage)

        # Calculate the amount of pixels to crop from each side
        crop_left = ((width - new_width) // 2) + int(shift_right * width)
        crop_top = ((height - new_height) // 2) + int(shift_down * height)
        crop_right = (width - crop_left - new_width)
        crop_bottom = (height - crop_top - new_height)

        # Crop the image
        cropped_image = image.crop((crop_left, crop_top, width - crop_right, height - crop_bottom))

        # Resize the cropped image to the desired dimensions
        resized_image = cropped_image.resize((new_width, new_height))

        # Save the resized image over the original file
        resized_image.save(image_save)
        if flip:
            shift_right = shift_right * -1