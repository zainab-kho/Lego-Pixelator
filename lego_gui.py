# Lego Pixelator
# The Main Thread: Madelyn Jeffers, Zainab Khoshnaw
# Description: # Lego Pixelator
# The Main Thread: Madelyn Jeffers, Zainab Khoshnaw
# Description: This project is an image processor that turns normal images into a pixelated lego-like 
#   veresion. It works by analyzing the original image pixel by pixel and grouping them into color 
#   blocks, making the image look like it’s made out of lego bricks.

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageDraw
from Lego_Pixelator_Slicing import slice_image_into_grid
from Lego_Pixelator_Average_Colors import get_lego_pixel_blocks
from Lego_Pixelator_Main import assemble_image

grid_size = (48, 48)

class LegoApp:
    """
    A tkinter-based GUI for the Lego Pixelator Project.
    Allows users to upload an image, pixelate it into LEGO-style blocks,
    preview it, and save the result to disk
    """
    def __init__(self, root):
        """
        Initialize the GUI elements, including buttons, image and layout
        setup for the Lego Pixelator app.
        """
        self.root = root
        self.root.title("Lego Pixelator")
        self.root.geometry("430x430") # width x height

        # title
        self.label = tk.Label(root, text="Welcome to Lego Pixelator", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Upload Image", font=("Helvetica", 12), command=self.upload_image)
        self.upload_btn.pack()
        
        # create blank placeholder image
        placeholder = Image.new('RGB', (200, 260), color='#dddddd')
        draw = ImageDraw.Draw(placeholder)
        draw.text((80, 90), "No Image", fill="gray")
        self.tk_img = ImageTk.PhotoImage(placeholder)

        self.preview = tk.Label(root, image=self.tk_img)
        self.preview.pack(pady=10)

        # horizontal row for "Pixelate" amd "Save" buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.process_btn = tk.Button(button_frame, text="Pixelate It!", font=("Helvetica", 12), command=self.pixelate_image, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=5)

        # save photo button
        self.save_btn = tk.Button(button_frame, text="Save Photo", font=("Helvetica", 12), command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # close app
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def upload_image(self):
        """
        Handles image upload and preview:
        - Opens file dialog
        Fixes EXIF orientation
        Resizes image for preview
        Stores path to corrected image
        """
        # disable save photo button again
        self.save_btn.config(state=tk.DISABLED)   
                
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            # open and fix orientation first
            img = Image.open(file_path)
            img = ImageOps.exif_transpose(img)

            # save the corrected version for processing
            rotated_path = "temp_fixed_image.png"
            img.save(rotated_path)
            self.img_path = rotated_path

            # resize preview to always be 800px wide (maintain aspect ratio)
            preview_width = 200
            aspect_ratio = img.height / img.width
            preview_height = int(preview_width * aspect_ratio)
            preview_img = img.resize((preview_width, preview_height), Image.LANCZOS)

            self.tk_img = ImageTk.PhotoImage(preview_img)
            self.preview.config(image=self.tk_img, text="")
            self.process_btn.config(state=tk.NORMAL)

    def pixelate_image(self):
        """
        Processes the uploaded image:
        - Slices it into a grid
        - Converts blocks to LEGO colors
        - Assembles and upscales the final image
        - Displays the result and enables save
        """
        # disable button while pixelating
        self.process_btn.config(state=tk.DISABLED)
        
        blocks = slice_image_into_grid(self.img_path, grid_size)
        lego_blocks = get_lego_pixel_blocks(blocks)
        final_img = assemble_image(lego_blocks, grid_size)

        # upscale final output to 800px wide
        if final_img.width < 800:
            scale_factor = 800 / final_img.width
            new_size = (int(final_img.width * scale_factor), int(final_img.height * scale_factor))
            final_img = final_img.resize(new_size, Image.NEAREST)

        self.final_img = final_img # save for export
        self.save_btn.config(state=tk.NORMAL) # enable the save button
        final_img.show()
        
    def save_image(self):
        """
        Opens a save dialog and saves the final pixelated image.
        only enabeld after pixelation is complete.
        """
        if hasattr(self, 'final_img'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.final_img.save(file_path)
                
    def quit_app(self):
        """
        Fully quits the app and closes the tkinter window.
        Ensures terminal is released after GUI closes.
        """
        self.root.destroy()
        exit() # ensures full exit, including from terminal
        
root = tk.Tk()
app = LegoApp(root)
root.resizable(False, False)
root.mainloop()
