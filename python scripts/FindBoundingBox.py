import os
import re
import time
from PIL import Image

# Function to find incremental bounding box
import numpy as np



def find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox=None):
    start_time = time.time()
    # if (last_bbox is None) or (last_bbox == (0,0,0,0,0,0)):
    #     left, top, right, bottom = 0, 0, image.width, image.height
    # else:
    #     left, top, right, bottom, _, _ = last_bbox
    left, top, right, bottom = 0, 0, image.width, image.height
    width, height = image.size

    # Extract columns of pixels for the borders
    left_column = np.array([image.getpixel((left, y)) for y in range(top, bottom-1)])
    right_column = np.array([image.getpixel((min(width-1,right-1), y)) for y in range(top, bottom-1)])
    top_row = np.array([image.getpixel((x, top)) for x in range(left, right-1)])
    bottom_row = np.array([image.getpixel((x, min(height-1, bottom-1))) for x in range(left, right-1)])

    if np.all((right_column >= background_min_RGB) & (right_column <= background_max_RGB)):

        right_grow_direction = -1
    else:
        right_grow_direction = 1

    if np.all((left_column >= background_min_RGB) & (left_column <= background_max_RGB)):

        left_grow_direction = 1
    else:
        left_grow_direction = -1

    if np.all((top_row >= background_min_RGB) & (top_row <= background_max_RGB)):

        top_grow_direction = 1
    else:
        top_grow_direction = -1

    if np.all((bottom_row>= background_min_RGB) & (bottom_row <= background_max_RGB)):
        
        bottom_grow_direction = -1
    else:
        bottom_grow_direction = 1

    while right >= 0 and right <= width:
        right_column = np.array([image.getpixel((right-1, y)) for y in range(top, bottom-1)])
        background = np.all((right_column >= background_min_RGB) & (right_column <= background_max_RGB))
        if (right_grow_direction == 1 & background) or (right_grow_direction == -1 and not background):
            break                               
        right += step_length * right_grow_direction

    while left >= 0 and left < width:
        left_column = np.array([image.getpixel((left, y)) for y in range(top, bottom-1)])
        background = np.all((left_column >= background_min_RGB) & (left_column <= background_max_RGB))
        if (left_grow_direction == -1 and background) or (left_grow_direction == 1 and not background):
            break
        left += step_length * left_grow_direction

    while top >= 0 and top < height:
        top_row = np.array([image.getpixel((x, top-1)) for x in range(left, right-1)])
        background = np.all((top_row >= background_min_RGB) & (top_row <= background_max_RGB))
        if (top_grow_direction == -1 and background) or (top_grow_direction == 1 and not background):
            break
        top += step_length * top_grow_direction

    while bottom > 0 and bottom <= height:
        bottom_row = np.array([image.getpixel((x, bottom-1)) for x in range(left, right-1)])
        background = np.all((bottom_row >= background_min_RGB) & (bottom_row <= background_max_RGB))
        if (bottom_grow_direction == 1 and background) or (bottom_grow_direction == -1 and not background):
            break
        bottom += step_length * bottom_grow_direction


    new_width = right - left
    new_height = bottom - top
    print ("Time:", time.time() - start_time)
    print("Left:", left)
    print("Top:", top)
    print("Right:", right)
    print("Bottom:", bottom)
    print("New Width:", new_width)
    print("New Height:", new_height)

    return left, top, right, bottom, new_width, new_height

def save_resized_image(image, image_save, last_bbox):
    left, top, right, bottom, new_width, new_height = last_bbox

    # Crop the image using the incremental bounding box
    cropped_image = image.crop((left, top, right, bottom))

    # Resize the cropped image to the desired dimensions
    resized_image = cropped_image.resize((new_width, new_height))
    resized_image.save(image_save)

def save_multiple(src_path, save_path, startfile, endfile, background_min_RGB, background_max_RGB, step_length):

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


        last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1
        # last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length, last_bbox)
        # counter+=1

        print(f"bbox:{counter} = {last_bbox}")
        save_resized_image(image, image_save, last_bbox)

        if counter == endfile:
            break


def save_single(src_path,filename, save_path, background_min_RGB, background_max_RGB, step_length) :

    image = Image.open(src_path + filename)

    left, top, right, bottom = 0, 0, image.size[0], image.size[1]
    last_bbox = (left, top, right, bottom, 1284, 2009)
    last_bbox = find_incremental_bounding_box(image, background_min_RGB, background_max_RGB, step_length)

    image_save = save_path + filename

    save_resized_image(image, image_save, last_bbox)


if __name__ == "__main__":
    save_multiple("cropinput/", "cropoutput/", startfile=0, endfile=300, background_min_RGB=250, background_max_RGB=255, step_length=1)
    # compare("cropinput/","page_007.jpg")
    # image = Image.open("cropinput/page_006.jpg")
    # save_resized_image(image, "testimage/page_006.jpg", (120, 344, 2087, 2695, 1968, 2352))