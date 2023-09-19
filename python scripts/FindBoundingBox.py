import os
import re
import time
from PIL import Image

# Function to find incremental bounding box
import numpy as np



def find_incremental_bounding_box(image, last_bbox, bacground_min_RGB, background_max_RGB, step_length, ):
    left, top, right, bottom, _, _ = last_bbox
    width, height = image.size

    # Extract columns of pixels for the borders
    left_column = np.array([image.getpixel((left, y)) for y in range(bottom, top-1)])
    right_column = np.array([image.getpixel((right-1, y)) for y in range(bottom, top-1)])
    top_row = np.array([image.getpixel((x, top)) for x in range(left, right-1)])
    bottom_row = np.array([image.getpixel((x, bottom-1)) for x in range(left, right-1)])

    if ((np.any(np.array(right_column) <= bacground_min_RGB)) or (np.any(np.array(right_column) >= background_max_RGB))):

        right_grow_direction = 1
    else:
        right_grow_direction = -1

    if ((np.any(np.array(left_column) <= bacground_min_RGB)) or (np.any(np.array(left_column) >= background_max_RGB))):

        left_grow_direction = -1
    else:
        left_grow_direction = 1

    if ((np.any(np.array(top_row) <= bacground_min_RGB)) or (np.any(np.array(top_row) >= background_max_RGB))):

        top_grow_direction = -1
    else:
        top_grow_direction = 1

    if ((np.any(np.array(bottom_row) <= bacground_min_RGB)) or (np.any(np.array(bottom_row) >= background_max_RGB))):
        
        bottom_grow_direction = 1
    else:
        bottom_grow_direction = -1

    while right >= 0 & right <= width+1:
        right_column = np.array([image.getpixel((right-1, y)) for y in range(bottom, top-1)])
        not_background = np.any((right_column <= bacground_min_RGB) | (right_column >= background_max_RGB))
        if (not_background & right_grow_direction == -1) or ((not not_background) & right_grow_direction == 1) :
            break
        right += step_length * right_grow_direction

    while left >= 0 and left <= width:
        left_column = np.array([image.getpixel((left, y)) for y in range(bottom, top-1)])
        not_background = np.any((left_column <= bacground_min_RGB) | (left_column >= background_max_RGB))
        if (not_background and left_grow_direction == 1) or ((not not_background) and left_grow_direction == -1):
            break
        left += step_length * left_grow_direction


    while top >= 0 and top <= height:
        top_row = np.array([image.getpixel((x, top-1)) for x in range(left, right-1)])
        not_background = np.any((top_row <= bacground_min_RGB) | (top_row >= background_max_RGB))
        if (not_background and top_grow_direction == 1) or ((not not_background) and top_grow_direction == -1):
            break
        top += step_length * top_grow_direction

    while bottom >= 0 and bottom <= height:
        bottom_row = np.array([image.getpixel((x, bottom)) for x in range(left, right-1)])
        not_background = np.any((bottom_row <= bacground_min_RGB) | (bottom_row >= background_max_RGB))
        if (not_background and bottom_grow_direction == -1) or ((not not_background) and bottom_grow_direction == 1):
            break
        bottom += step_length * bottom_grow_direction


    new_width = right - left
    new_height = bottom - top
    print("Left:", left)
    print("Bottom:", bottom)
    print("Right:", right)
    print("Top:", top)
    print("New Width:", new_width)
    print("New Height:", new_height)

    return left, top, right, bottom, new_width, new_height



def find_smallest_bounding_box(image, bacground_min_RGB, background_max_RGB):
    width, height = image.size
    left, top, right, bottom = 0, 0, width, height

    # Scan each pixel to find the bounding box
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if ((np.any(np.array(pixel) <= bacground_min_RGB)) or (np.any(np.array(pixel) >= background_max_RGB))):
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

def save_multiple(src_path, save_path, startfile, endfile):

    files = os.listdir(src_path)

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

        _, file_extension = os.path.splitext(filename)
        if file_extension.lower() not in {".jpg", ".jpeg", ".png"}:
            continue

        if counter < startfile:
            continue

        image_path = os.path.join(src_path, filename)
        image_save = os.path.join(save_path, filename)

        try:
            image = Image.open(image_path)
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




def save_single(src_path,filename, save_path) :

    image = Image.open(src_path + filename)

    left, top, right, bottom = 0, 0, image.size[0], image.size[1]
    last_bbox = find_incremental_bounding_box(image,last_bbox=(left, top, right, bottom, 1284, 2009), bacground_min_RGB=250,background_max_RGB=300, step_length=1)

    image_save = save_path + filename

    save_resized_image(image, image_save, last_bbox)

def compare(src_path,filename):

    image = Image.open(src_path + filename)

    start_time = time.time()
    last_bbox = find_incremental_bounding_box(image,last_bbox=(0, 0, 0, 0, 0, 0), bacground_min_RGB=250,background_max_RGB=300, step_length=1)
    end_time = time.time()
    print(f"find_borders elapsed time: {end_time - start_time} seconds")
    print("incremental Bounding Box:", last_bbox)


    start_time = time.time()
    last_bbox = find_smallest_bounding_box(image, bacground_min_RGB=250,background_max_RGB=300)
    end_time = time.time()
    print(f"find_borders elapsed time: {end_time - start_time} seconds")
    print("smallest Bounding Box:", last_bbox)


if __name__ == "__main__":
    save_single("cropinput/", "page_006.jpg", "testimage")
    # compare("cropinput/","page_007.jpg")
    # image = Image.open("cropinput/page_006.jpg")
    # save_resized_image(image, "testimage/page_006.jpg", (120, 344, 2087, 2695, 1968, 2352))