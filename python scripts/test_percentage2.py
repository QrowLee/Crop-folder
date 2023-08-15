from PIL import Image

# Set the path to the folder containing the images
filename = "image-013.jpg"
save_path = "testimage/"
src_path = "cropinput/"
# Set the new dimensions for the cropped image
width_percentage = 0.93
height_percentage = 0.89
shift_right = 0.02
shift_down = 0.000
flip = False

# Open the original image
image = Image.open(src_path + filename)

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
resized_image.save(save_path + filename)
