from PIL import Image

# Set the path to the folder containing the images
filename = "The_Thirteenth_Floor_2_010.jpg"
save_path = "images/"
src_path = "images - Copy/"
# Set the new dimensions for the cropped image
width_percentage = 0.94
height_percentage = 0.9
shift_right = 0
shift_down = -0.02
flip = False

# Loop through every file in the folde
image = Image.open(src_path + filename)

# Get the original size of the image
width, height = image.size

# Calculate the new dimensions based on the percentage
new_width = int(width * width_percentage)
new_height = int(height * height_percentage)
shift_right = shift_right * new_width
shift_down = shift_right * new_height

# Calculate the amount of pixels to crop from each side
crop_left = ((width - new_width) // 2) + shift_right
crop_top = ((height - new_height) // 2) + shift_down
crop_right = (width - crop_left - new_width) - shift_right
crop_bottom = (height - crop_top - new_height) - shift_down

# Crop the image
cropped_image = image.crop((crop_left, crop_top, width - crop_right, height - crop_bottom))

# Resize the cropped image to the desired dimensions
resized_image = cropped_image.resize((new_width, new_height))

# Save the resized image over the original file
resized_image.save(save_path + filename)