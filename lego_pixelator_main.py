# Lego Pixelator
# The Main Thread: Madelyn Jeffers, Zainab Khoshnaw
# Description: This project is an image processor that turns normal images into a pixelated lego-like 
#   veresion. It works by analyzing the original image pixel by pixel and grouping them into color 
#   blocks, making the image look like it’s made out of lego bricks.

from PIL import Image

def assemble_image(blocks, grid_size):
    """
    Assembles a list of image blocks into one final image based on the blocks 
    and the grid size. Returns the final combined image.
    """
    if not blocks:
        print("ERROR: No blocks received.")
        return None

    expected = grid_size[0] * grid_size[1]
    if len(blocks) != expected:
        print(f"ERROR: Expected {expected} blocks, got {len(blocks)}")
        return None

    block_width, block_height = blocks[0].size
    total_width = grid_size[0] * block_width
    total_height = grid_size[1] * block_height

    final_img = Image.new('RGB', (total_width, total_height))

    for index, block in enumerate(blocks):
        row = index // grid_size[0]
        col = index % grid_size[0]
        x = col * block_width
        y = row * block_height
        final_img.paste(block, (x, y))

    return final_img
