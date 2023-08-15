import concurrent.futures
import time
from PIL import Image
import os

import concurrent.futures
from PIL import Image
import threading

def process_pixel(x, y, image, threshold, lock):
    width, height = image.size

    # Check if the pixel coordinates are within the image boundaries
    if x < 0 or x >= width or y < 0 or y >= height:
        return None

    with lock:
        pixel = image.getpixel((x, y))
    if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
        return x, y

    return None

def find_borders(image_path, threshold):
    image = Image.open(image_path)
    width, height = image.size
    left, top, right, bottom = width, height, 0, 0

    lock = threading.Lock()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        # Search for the top border
        for y in range(height):
            futures.append(executor.submit(process_pixel, 0, y, image, threshold, lock))
        
        # Search for the bottom border
        for y in range(height):
            futures.append(executor.submit(process_pixel, width - 1, y, image, threshold, lock))
        
        # Search for the left border
        for x in range(width):
            futures.append(executor.submit(process_pixel, x, 0, image, threshold, lock))
        
        # Search for the right border
        for x in range(width):
            futures.append(executor.submit(process_pixel, x, height - 1, image, threshold, lock))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                x, y = result
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    new_width = right - left + 1
    new_height = bottom - top + 1

    return left, top, right, bottom, new_width, new_height





def find_smallest_bounding_box(image_path, threshold):
    image = Image.open(image_path)
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

# def find_smallest_bounding_box(image, threshold):
#     width, height = image.size
#     left, top, right, bottom = width, height, 0, 0

#     # Lists to store the first pixels detected as non-white for each border
#     top_pixel, bottom_pixel, left_pixel, right_pixel = None, None, None, None

#     # Scan each pixel to find the bounding box
#     for x in range(width):
#         for y in range(height):
#             pixel = image.getpixel((x, y))
#             if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
#                 left = min(left, x)
#                 top = min(top, y)
#                 right = max(right, x)
#                 bottom = max(bottom, y)

#                 # Store the first non-white pixels for each border
#                 if top_pixel is None and y == top:
#                     top_pixel = pixel, (x, y)
#                 if bottom_pixel is None and y == bottom:
#                     bottom_pixel = pixel, (x, y)
#                 if left_pixel is None and x == left:
#                     left_pixel = pixel, (x, y)
#                 if right_pixel is None and x == right:
#                     right_pixel = pixel, (x, y)

#     new_width = right - left + 1
#     new_height = bottom - top + 1

#     print("First Pixel Detected as Non-White for Each Border:")
#     if top_pixel:
#         print(f"Top Border: RGB: {top_pixel[0]}, XY Position: {top_pixel[1]}")
#     if bottom_pixel:
#         print(f"Bottom Border: RGB: {bottom_pixel[0]}, XY Position: {bottom_pixel[1]}")
#     if left_pixel:
#         print(f"Left Border: RGB: {left_pixel[0]}, XY Position: {left_pixel[1]}")
#     if right_pixel:
#         print(f"Right Border: RGB: {right_pixel[0]}, XY Position: {right_pixel[1]}")

#     return left, top, right, bottom, new_width, new_height



def save_resized_image(image, image_save, last_bbox):
    left, top, right, bottom, new_width, new_height = last_bbox

    # Crop the image using the incremental bounding box
    cropped_image = image.crop((left, top, right, bottom))

    # Resize the cropped image to the desired dimensions
    resized_image = cropped_image.resize((new_width, new_height))
    resized_image.save(image_save)

def save_single():
    filename = "testbanana.jpg"
    save_path = "testimage/"
    image_save = save_path + filename
    image_path = "cropinput/AdvRSVol1_Page_123.jpg"


    start_time = time.time()
    borders_bbox = find_borders(image_path, threshold=245)
    end_time = time.time()
    print(f"find_borders elapsed time: {end_time - start_time} seconds")
    print("Borders Bounding Box:", borders_bbox)

    start_time = time.time()
    smallest_bbox = find_smallest_bounding_box(image_path, threshold=245)
    end_time = time.time()
    print(f"find_smallest_bounding_box elapsed time: {end_time - start_time} seconds")
    print("Smallest Bounding Box:", smallest_bbox)

    # image_save = save_path + filename

    # save_resized_image(image, image_save, smallest_bbox)

if __name__ == "__main__":
    save_single()