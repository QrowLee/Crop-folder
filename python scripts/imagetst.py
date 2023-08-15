from PIL import Image

def print_key_pixels(image):
    width, height = image.size
    key_pixels = [
        (0, 0),                      # Top-left corner
        (width - 1, 0),              # Top-right corner
        (0, height - 1),             # Bottom-left corner
        (width - 1, height - 1),     # Bottom-right corner
        (width // 2, height // 2),   # Center pixel
        (width // 4, height // 4),   # Top-left quadrant pixel
        (3 * width // 4, height // 4) # Top-right quadrant pixel
    ]

    print("Key Pixels:")
    for x, y in key_pixels:
        pixel = image.getpixel((x, y))
        print(f"Pixel at ({x}, {y}): RGB = {pixel}")

# Example usage:
image_path = "cropinput/image-124.jpg"
image = Image.open(image_path)

# Print the RGB values of key pixels in the image
print_key_pixels(image)
