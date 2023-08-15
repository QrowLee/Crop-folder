from PIL import Image

# Open the original image
image = Image.open("images - Copy/page016.jpg")

# Get the original size of the image
width, height = image.size

# Set the new size for the cropped image
new_width = 1010
new_height = 1520
shift_right = -12
shift_down = -24

# Calculate the amount of pixels to crop from each side
crop_left = ((width - new_width) // 2) + shift_right
crop_top = ((height - new_height) // 2 )+ shift_down
crop_right = (width - crop_left - new_width) - shift_right
crop_bottom = (height - crop_top - new_height) - shift_down

# Crop the image
cropped_image = image.crop((crop_left, crop_top, width - crop_right, height - crop_bottom))

# Resize the cropped image to the desired dimensions
resized_image = cropped_image.resize((new_width, new_height))

# Save the resized image
resized_image.save("resized_image.jpg")
