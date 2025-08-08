# Lego Pixelator

## Description:

A Python desktop application that turns ordinary images into stylized LEGO blocks.
Users can upload an image, preview it, pixelate it using LEGO-like bricks, and save the result.

## Built By
- Zainab Khoshnaw
- Madelyn Jeffers

## Features
- GUI built with `tkinter` for easy use
- Image orientation automatically corrected (EXIF support)
- Image is sliced into a 48x48 grid and averaged by color
- Each block is replaced with the closest matching LEGO color
- Blocks have shading and 3D “studs” to resemble real LEGO pieces
- Final image is upscaled and viewable
- Users can save the output as a `.png` file
- Users can view a list of all lego bricks used and how many

## How It Works
1. User opens the app and uploads an image
2. A preview of the image appears in the app
3. Clicking **"Pixelate It!"** runs the processing
4. The result is displayed and can be saved with **"Save Photo"**
5. The block list is displayed with **"Show Brick Stats"**

## Requirements
- Python 3.7+
- `pillow`
- `numpy`
- `tkinter` (comes built-in with Python)

Install dependencies:
```bash
pip install pillow numpy
