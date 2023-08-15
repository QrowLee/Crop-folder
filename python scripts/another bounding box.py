import os
from PIL import Image

def find_incremental_bounding_box(image, last_bbox, threshold=250, max_expansion=20):
    left, top, right, bottom = last_bbox
    width, height = image.size

    for x in range(max(left - max_expansion, 0), left):
        for y in range(top, bottom + 1):
            pixel = image.getpixel((x, y))
            if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
                left = x
                break
        else:
            break

    # Check for non-white pixels on the right border
    for x in range(min(right + max_expansion, width - 1), right, -1):
        for y in range(top, bottom + 1):
            pixel = image.getpixel((x, y))
            if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
                right = x
                break
        else:
            break

    # Check for non-white pixels on the top border
    for y in range(max(top - max_expansion, 0), top):
        for x in range(left, right + 1):
            pixel = image.getpixel((x, y))
            if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
                top = y
                break
        else:
            break

    # Check for non-white pixels on the bottom border
    for y in range(min(bottom + max_expansion, height - 1), bottom, -1):
        for x in range(left, right + 1):
            pixel = image.getpixel((x, y))
            if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
                bottom = y
                break
        else:
            break

    if left == right or top == bottom:
        raise ValueError("No non-white pixels found in the image.")

    return left, top, right, bottom

def crop_and_save_images(src_folder, save_folder, num_images, threshold=200, max_expansion=20):
    # Get the list of image files in the source folder
    files = os.listdir(src_folder)

    # Ensure that the number of images to process does not exceed the available images
    num_images = min(num_images, len(files))

    # Get the bounding box of the first image
    image_path = os.path.join(src_folder, files[0])
    image = Image.open(image_path)
    initial_bbox = (0, 0, image.width - 1, image.height - 1)

    # Process each image in the specified range
    for i in range(num_images):
        filename = files[i]
        image_path = os.path.join(src_folder, filename)
        image_save = os.path.join(save_folder, filename)
        image = Image.open(image_path)

        # Find the incremental bounding box coordinates using the threshold and previous bounding box
        if i == 0:
            bbox = initial_bbox
        else:
            bbox = find_incremental_bounding_box(image, bbox, threshold=threshold, max_expansion=max_expansion)

        # Crop the image using the incremental bounding box
        cropped_image = image.crop((bbox[0], bbox[1], bbox[2] + 1, bbox[3] + 1))  # Adding 1 to right and bottom to include the last pixel

        # Save the cropped and resized image
        cropped_image.save(image_save)

# Example usage:
src_folder = "cropinput"
save_folder = "output"
num_images = 20  # Set the number of images to process

# Threshold value (adjust as needed)
threshold_value = 200
# Maximum expansion value (adjust as needed)
max_expansion_value = 100000000

crop_and_save_images(src_folder, save_folder, num_images, threshold=threshold_value, max_expansion=max_expansion_value)
