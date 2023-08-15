import os
import re
import time
from PIL import Image

# Function to find incremental bounding box
import numpy as np



def find_incremental_bounding_box(image, last_bbox, threshold, step_length):
    left, top, right, bottom, _, _ = last_bbox
    width, height = image.size

    # Extract columns of pixels for the left and right borders
    left_column = np.array([image.getpixel((left, y)) for y in range(top, bottom + 1)])
    right_column = np.array([image.getpixel((right, y)) for y in range(top, bottom + 1)])

    # Check if there are non-white pixels in the left and right columns
    left_border_grow = np.any(np.logical_and(left_column[:, 0] <= threshold,
                                             left_column[:, 1] <= threshold,
                                             left_column[:, 2] <= threshold))

    right_border_grow = np.any(np.logical_and(right_column[:, 0] <= threshold,
                                              right_column[:, 1] <= threshold,
                                              right_column[:, 2] <= threshold))
    
    # Extract rows of pixels for the top and bottom borders
    top_row = np.array([image.getpixel((x, top)) for x in range(left, right + 1)])
    bottom_row = np.array([image.getpixel((x, bottom)) for x in range(left, right + 1)])

    # Check if there are non-white pixels in the top and bottom rows
    top_border_grow = np.any(np.logical_and(top_row[:, 0] <= threshold,
                                            top_row[:, 1] <= threshold,
                                            top_row[:, 2] <= threshold))

    bottom_border_grow = np.any(np.logical_and(bottom_row[:, 0] <= threshold,
                                               bottom_row[:, 1] <= threshold,
                                               bottom_row[:, 2] <= threshold))

    # Search for the new left border position to grow or shrink
    if left_border_grow:
        while left > 0:
            left_column = np.array([image.getpixel((left, y)) for y in range(top, bottom + 1)])
            if not np.any(np.logical_and(left_column[:, 0] <= threshold,
                                         left_column[:, 1] <= threshold,
                                         left_column[:, 2] <= threshold)):
                break
            left -= step_length
    else:
        while left < right:
            left_column = np.array([image.getpixel((left, y)) for y in range(top, bottom + 1)])
            if     np.any(np.logical_and(left_column[:, 0] <= threshold,
                                        left_column[:, 1] <= threshold,
                                        left_column[:, 2] <= threshold)):
                break
            left += step_length

    if right_border_grow:
        while right < width - 1:
            right_column = np.array([image.getpixel((right, y)) for y in range(top, bottom + 1)])
            if not np.any(np.logical_and(right_column[:, 0] <= threshold,
                                        right_column[:, 1] <= threshold,
                                        right_column[:, 2] <= threshold)):
                break
            right += step_length
    else:
        while right > left:
            right_column = np.array([image.getpixel((right, y)) for y in range(top, bottom + 1)])
            if np.any(np.logical_and(right_column[:, 0] <= threshold,
                                    right_column[:, 1] <= threshold,
                                    right_column[:, 2] <= threshold)):
                break
            right -= step_length


    if top_border_grow:
        while top > 0:
            top_row = np.array([image.getpixel((x, top)) for x in range(left, right + 1)])
            if not np.any(np.logical_and(top_row[:, 0] <= threshold,
                                        top_row[:, 1] <= threshold,
                                        top_row[:, 2] <= threshold)):
                break
            top -= step_length
    else:
        while top < bottom:
            top_row = np.array([image.getpixel((x, top)) for x in range(left, right + 1)])
            if np.any(np.logical_and(top_row[:, 0] <= threshold,
                                    top_row[:, 1] <= threshold,
                                    top_row[:, 2] <= threshold)):
                break
            top += step_length


    if bottom_border_grow:
        while bottom < height - 1:
            bottom_row = np.array([image.getpixel((x, bottom)) for x in range(left, right + 1)])
            if not np.any(np.logical_and(bottom_row[:, 0] <= threshold,
                                        bottom_row[:, 1] <= threshold,
                                        bottom_row[:, 2] <= threshold)):
                break
            bottom += step_length
    else:
        while bottom > top:
            bottom_row = np.array([image.getpixel((x, bottom)) for x in range(left, right + 1)])
            if np.any(np.logical_and(bottom_row[:, 0] <= threshold,
                                    bottom_row[:, 1] <= threshold,
                                    bottom_row[:, 2] <= threshold)):
                break
            bottom -= step_length


    new_width = right - left + 1
    new_height = bottom - top + 1

    return left, top, right, bottom, new_width, new_height



def find_smallest_bounding_box(image, threshold):
    width, height = image.size
    left, top, right, bottom = width, height, 0, 0

    # Scan each pixel to find the bounding box
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    new_width = right - left + 1
    new_height = bottom - top + 1

    return left, top, right, bottom, new_width, new_height


def save_resized_image(image, image_save, last_bbox):
    left, top, right, bottom, new_width, new_height = last_bbox

    # Crop the image using the incremental bounding box
    cropped_image = image.crop((left, top, right, bottom))

    # Resize the cropped image to the desired dimensions
    resized_image = cropped_image.resize((new_width, new_height))
    resized_image.save(image_save)

def save_multiple():

    src_path = "cropinput"
    save_path = "cropoutput"

    files = os.listdir(src_path)

    startfile = 0
    endfile = 5000

    pgnumbers = []
    pattern = r"\d+"

    sortFilesByName = False
    # Loop through the files in the folder
    if sortFilesByName:
        for filename in files:
            pgname, file_extension = os.path.splitext(filename)
            if file_extension.lower() in {".jpg", ".jpeg", ".png"}:
                match = re.search(pattern, pgname)
                if match:
                    pg_number = int(match.group())
                    pgnumbers.append((pg_number, filename))

        files = [filename for _, filename in sorted(pgnumbers)]

    last_bbox = (0, 0, 0, 0, 0, 0)  # Initialize last_bbox with all zeros


    for counter, filename in enumerate(files, start=startfile):
        print(filename)

        _, file_extension = os.path.splitext(filename)
        if file_extension.lower() not in {".jpg", ".jpeg", ".png"}:
            continue

        if counter < startfile:
            continue

        image_path = os.path.join(src_path, filename)
        image_save = os.path.join(save_path, filename)

        try:
            image = Image.open(image_path)
            print(image_path)
            print(image)
        except IOError:
            print(f"Error opening image: {image_path}")
            continue

        if last_bbox == (0, 0, 0, 0, 0, 0):
            last_bbox = find_smallest_bounding_box(image, threshold=250)
        else:
            last_bbox = find_incremental_bounding_box(image, last_bbox, threshold=250, step_length= 1)

        print(f"bbox:{counter} = {last_bbox}")
        save_resized_image(image, image_save, last_bbox)

        if counter == endfile:
            break

def print_filenames():
    import os

    src_path = "cropinput"

    files = os.listdir(src_path)

    for filename in files:
        _, file_extension = os.path.splitext(filename)
        if file_extension.lower() in {".jpg", ".jpeg", ".png"}:
            print(filename)




def save_single():
    filename = "image-045.jpg"
    save_path = "testimage/"
    src_path = "cropinput/"

    image = Image.open(src_path + filename)

    last_bbox = find_incremental_bounding_box(image,last_bbox=(45, 90, 1350, 2090, 1284, 2009), threshold=250, )

    image_save = save_path + filename

    save_resized_image(image, image_save, last_bbox)

def compare():
    filename = "page100.jpg"
    save_path = "testimage/"
    src_path = "cropinput/"

    image = Image.open(src_path + filename)

    start_time = time.time()
    last_bbox = find_incremental_bounding_box(image,last_bbox=(0, 0, 0, 0, 0, 0), threshold=250, step_length=1)
    end_time = time.time()
    print(f"find_borders elapsed time: {end_time - start_time} seconds")
    print("incremental Bounding Box:", last_bbox)


    start_time = time.time()
    last_bbox = find_smallest_bounding_box(image, threshold=250)
    end_time = time.time()
    print(f"find_borders elapsed time: {end_time - start_time} seconds")
    print("smallest Bounding Box:", last_bbox)


if __name__ == "__main__":
    save_multiple()