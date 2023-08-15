import os
from PIL import Image

# Set the path to the folder containing the images
src_path = "images - Copy"
save_path = "images"
# Set the new dimensions for the cropped image
new_width = 2000
new_height = 3000
shift_right = -0
shift_down = -0
flip = False

# Loop through every file in the folder
for filename in os.listdir(src_path):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):

        # Open the original image
        image_path = os.path.join(src_path, filename)
        image_save = os.path.join(save_path, filename)
        image = Image.open(image_path)

        # Get the original size of the image
        width, height = image.size

        # Calculate the amount of pixels to crop from each side
        crop_left = ((width - new_width) // 2) + shift_right
        crop_top = ((height - new_height) // 2 )+ shift_down
        crop_right = (width - crop_left - new_width) - shift_right
        crop_bottom = (height - crop_top - new_height) - shift_down

        # Crop the image
        cropped_image = image.crop((crop_left, crop_top, width - crop_right, height - crop_bottom))

        # Resize the cropped image to the desired dimensions
        resized_image = cropped_image.resize((new_width, new_height))

        # Save the resized image over the original file
        resized_image.save(image_save)
        if flip:
            shift_right = shift_right * -1
