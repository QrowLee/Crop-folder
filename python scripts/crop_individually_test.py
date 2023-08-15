import os
from PIL import Image

# Set the new dimensions for the cropped image
right_percentage = 0.0725
left_percentage = 0.0325
top_percentage = 0.07
bottom_percentage = 0.08

input_folder = "cropinput/"
output_folder = "cropoutput/"
filename = "0014.jpg"

if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):

    image = Image.open(input_folder + filename)

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
    resized_image.save(output_folder + filename)