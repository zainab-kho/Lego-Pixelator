# Lego Pixelator
# The Main Thread: Madelyn Jeffers, Zainab Khoshnaw
# Description: This project is an image processor that turns normal images into a pixelated lego-like
#   version. It works by analyzing the original image pixel by pixel and grouping them into color
#   blocks, making the image look like it’s made out of lego bricks.

from PIL import Image #import the Pillow library

# slicing an image into a 48x48
def slice_image_into_grid(image_path, grid_size=(48, 48)):
    """ 
    Sicing an image into a 48x48
    """
    try:
        #open image and print the original dimensions
        img = Image.open(image_path)
        img_width, img_height = img.size
        print(f"Original image dimensions: {img_width}x{img_height}")

        #calculate block dimensions
        block_width = img_width // grid_size[0]
        block_height = img_height // grid_size[1]

        #handle image being too small
        if block_width == 0 or block_height == 0:
            print(f"Error: Image is too small to be divided into a {grid_size[0]}x{grid_size[1]} grid. "
                  f"Minimum dimensions for this grid size would be {grid_size[0]}x{grid_size[1]} pixels.")
            return []

        print(f"Each grid cell will be approximately {block_width}x{block_height} pixels.")

        sliced_images = []
        for r in range(grid_size[1]): #iterate through rows
            for c in range(grid_size[0]): #iterate through columns
                left = c * block_width
                top = r * block_height
                right = left + block_width
                bottom = top + block_height

                #ensure it doesn't go out of bounds for the last row/column due to integer division
                if c == grid_size[0] - 1:
                    right = img_width
                if r == grid_size[1] - 1:
                    bottom = img_height

                box = (left, top, right, bottom)
                tile = img.crop(box)
                sliced_images.append(tile)
        print(f"Image successfully sliced into {len(sliced_images)} pieces ({grid_size[0]}x{grid_size[1]} grid).")
        return sliced_images
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return []
    except Exception as e:
        print(f"An error occurred while slicing the image: {e}")
        return []
