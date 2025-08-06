import numpy as np
from PIL import Image, ImageDraw
from lego_colors import lego_colors

def hex_to_rgb(hex_color):
    """
    Converts a hex color string into an RGB tuple
    """
    hex_color = hex_color.strip().lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    """
    Calculates the Euclidean distance between two RGB color tuples
    """
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def find_closest_lego_rgb(rgb_color):
    """
    Finds and returns the RGB value of the closest LEGO color to the given RGB color
    """
    closest_rgb = None
    min_dist = float('inf')

    for hex_code in lego_colors:
        lego_rgb = hex_to_rgb(hex_code)
        dist = color_distance(rgb_color, lego_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_rgb = lego_rgb

    return closest_rgb

def draw_lego_stud(block, stud_color=None):
    """
    Draws a circulator LEGO stud on the given image block.
    If no stud color is given, it lightens the block color for the stud
    """
    draw = ImageDraw.Draw(block)
    w, h = block.size
    r = int(min(w, h) * 0.2)  # radius of stud

    cx, cy = w // 2, h // 2  # center
    bbox = [cx - r, cy - r, cx + r, cy + r]

    if not stud_color:
        stud_color = tuple(min(c + 30, 255) for c in block.getpixel((0, 0)))

    draw.ellipse(bbox, fill=stud_color)
    return block

def add_shading(block):
    """
    Apply a diagonal shading effect to give the block a plastic look
    """
    np_block = np.array(block)
    h, w, _ = np_block.shape

    for y in range(h):
        for x in range(w):
            factor = 1 - ((x + y) / (w + h)) * 0.2  # gradient
            np_block[y, x] = (np_block[y, x] * factor).astype(np.uint8)

    return Image.fromarray(np_block)

def get_lego_pixel_blocks(img_list):
    """
    Process a list of image tiles and gets average color,
    maps it to a LEGO color, and returns a list of styled image blocks
    """
    solid_blocks = []

    for i, img in enumerate(img_list):
        if img.mode != 'RGB':
            img = img.convert('RGB')
        np_img = np.array(img)
        avg_color = tuple(np_img.mean(axis=(0, 1)).astype(int))
        closest_rgb = find_closest_lego_rgb(avg_color)

        # create solid color block
        block = Image.new('RGB', img.size, closest_rgb)
        block = add_shading(block)
        block = draw_lego_stud(block)

        solid_blocks.append(block)

    return solid_blocks
