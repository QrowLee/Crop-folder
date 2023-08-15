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
        new_left = max(left - step_length, 0)
        whileCounter = 0
        while new_left < left:
            left_column = np.array([image.getpixel((new_left, y)) for y in range(top, bottom + 1)])
            if not np.any(np.logical_and(left_column[:, 0] <= threshold,                         left_column[:, 1] <= threshold,                                         left_column[:, 2] <= threshold)):
                print("left grown border reached at " + str(whileCounter))
                break
            left = new_left
            new_left = max(left - step_length, 0)
            whileCounter+=1
            print("whileCount = " + str(whileCounter))
    else:
        new_left = min(left + step_length, width - 1)
        while new_left > left:
            left_column = np.array([image.getpixel((new_left, y)) for y in range(top, bottom + 1)])
            if np.any(np.logical_and(left_column[:, 0] <= threshold,
                                     left_column[:, 1] <= threshold,
                                     left_column[:, 2] <= threshold)):
                break
            left = new_left
            new_left = min(left + step_length, width - 1)

    # Search for the new right border position to grow or shrink
    if right_border_grow:
        new_right = min(right + step_length, width - 1)
        while new_right > right:
            right_column = np.array([image.getpixel((new_right, y)) for y in range(top, bottom + 1)])
            if not np.any(np.logical_and(right_column[:, 0] <= threshold,
                                         right_column[:, 1] <= threshold,
                                         right_column[:, 2] <= threshold)):
                break
            right = new_right
            new_right = min(right + step_length, width - 1)
    else:
        new_right = max(right - step_length, 0)
        while new_right < right:
            right_column = np.array([image.getpixel((new_right, y)) for y in range(top, bottom + 1)])
            if np.any(np.logical_and(right_column[:, 0] <= threshold,
                                     right_column[:, 1] <= threshold,
                                     right_column[:, 2] <= threshold)):
                break
            right = new_right
            new_right = max(right - step_length, 0)

    # Search for the new top border position to grow or shrink
    if top_border_grow:
        new_top = max(top - step_length, 0)
        while new_top < top:
            top_row = np.array([image.getpixel((x, new_top)) for x in range(left, right + 1)])
            if not np.any(np.logical_and(top_row[:, 0] <= threshold,
                                         top_row[:, 1] <= threshold,
                                         top_row[:, 2] <= threshold)):
                break
            top = new_top
            new_top = max(top - step_length, 0)
    else:
        new_top = min(top + step_length, height - 1)
        while new_top > top:
            top_row = np.array([image.getpixel((x, new_top)) for x in range(left, right + 1)])
            if np.any(np.logical_and(top_row[:, 0] <= threshold,
                                     top_row[:, 1] <= threshold,
                                     top_row[:, 2] <= threshold)):
                break
            top = new_top
            new_top = min(top + step_length, height - 1)

    # Search for the new bottom border position to grow or shrink
    if bottom_border_grow:
        new_bottom = min(bottom + step_length, height - 1)
        while new_bottom > bottom:
            bottom_row = np.array([image.getpixel((x, new_bottom)) for x in range(left, right + 1)])
            if not np.any(np.logical_and(bottom_row[:, 0] <= threshold,
                                         bottom_row[:, 1] <= threshold,
                                         bottom_row[:, 2] <= threshold)):
                break
            bottom = new_bottom
            new_bottom = min(bottom + step_length, height - 1)
    else:
        new_bottom = max(bottom - step_length, 0)
        while new_bottom < bottom:
            bottom_row = np.array([image.getpixel((x, new_bottom)) for x in range(left, right + 1)])
            if np.any(np.logical_and(bottom_row[:, 0] <= threshold,
                                     bottom_row[:, 1] <= threshold,
                                     bottom_row[:, 2] <= threshold)):
                break
            bottom = new_bottom
            new_bottom = max(bottom - step_length, 0)

    new_width = right - left + 1
    new_height = bottom - top + 1

    return left, top, right, bottom, new_width, new_height

# Usage example:
# new_last_bbox = find_borders(image, last_bbox, threshold=250, step_length=500)