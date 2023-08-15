from PIL import Image

def find_smallest_bounding_box(image, threshold=250):
    width, height = image.size
    left, top, right, bottom = width, height, 0, 0
    bounding_box_pixels = []

    # Scan each pixel to find the bounding box
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel[0] <= threshold and pixel[1] <= threshold and pixel[2] <= threshold:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)
                #bounding_box_pixels.append((x, y, pixel))

    return left, top, right, bottom, bounding_box_pixels

# Example usage:
image_path = "cropinput/image-097.jpg"
image = Image.open(image_path)

# Threshold value (adjust as needed)
threshold_value = 200

# Find the bounding box coordinates and bounding box pixels using the threshold
left, top, right, bottom, bounding_box_pixels = find_smallest_bounding_box(image, threshold=threshold_value)

# Print the bounding box coordinates
print(f"Bounding Box Coordinates: (Left: {left}, Top: {top}, Right: {right}, Bottom: {bottom})")

# Print the position and RGB values of the pixels that define the bounding box
#print("Bounding Box Pixels:")
#for x, y, pixel in bounding_box_pixels:
#    print(f"Pixel at ({x}, {y}): RGB = {pixel}")

# Crop the image using the bounding box
cropped_image = image.crop((left, top, right + 1, bottom + 1))  # Adding 1 to right and bottom to include the last pixel

# Save or further process the cropped_image as needed
cropped_image.save("testimage/cropped_image2.jpg")




