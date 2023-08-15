import os
from PIL import Image

# Set the new dimensions for the cropped image
left_percentage = 0.0725
right_percentage = 0.0325
top_percentage = 0.06
bottom_percentage = 0.06

input_folder = "cropinput"
output_folder = "cropoutput"

flip = True
startfile = 0
endfile = 800

# Loop through every file in the folder

start_loop = 0
for filename in os.listdir(input_folder):

    if startfile <= start_loop <= endfile:
        # Check if the file is an image
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image = Image.open(os.path.join(input_folder, filename))

            image = Image.open(os.path.join(input_folder, filename))

            # Get the original size of the image
            width, height = image.size
            new_width = int(width - (width * (right_percentage + left_percentage)))
            new_height = int(height - (height * (top_percentage + bottom_percentage)))

            # Calculate the amount of pixels to crop from each side
            crop_left = width * left_percentage
            crop_top = height * top_percentage
            crop_right = width * right_percentage
            crop_bottom = height * bottom_percentage

            # Crop the image
            cropped_image = image.crop((crop_left, crop_top, width - crop_right, height - crop_bottom))

            # Resize the cropped image to the desired dimensions
            resized_image = cropped_image.resize((new_width, new_height))

            # Save the resized image over the original file
            resized_image.save(os.path.join(output_folder, filename))

            if flip:
                left_percentage, right_percentage = right_percentage, left_percentage

    start_loop += 1