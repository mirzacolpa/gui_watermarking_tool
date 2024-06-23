import tkinter as tk
from tkinter import Label, Button, ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import window_config as winconf
import watermark as wt


### Methods
def display_image(event):
    selected_index = listbox.curselection()
    if selected_index:
        image_path = listbox.get(selected_index)
        img = Image.open(image_path)
        # TODO: Define max and min size and save the definitions in window_config file
        # TODO: resize image to the aspect ratio
        # TODO: avoid resizing if the image is smaller than defined display size
        img = img.resize((800, 800))  # Resize the image to fit the right column
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img
        panel.image_path = image_path


def add_image_to_list(listbox_holder):
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    )
    if file_path:
        listbox_holder.insert(tk.END, file_path)


# TODO: implement remove logic for the loaded images
def remove_image_from_list():
    pass


def build_watermark_configuration():
    watermark = wt.Watermark(text=text_input_field.get(), font=font_picker.get(), fontsize=int(font_size_picker.get()),
                             color=color_picker.get(), opacity=int(opacity_picker.get()),
                             pos_x=int(position_x_picker.get()), pos_y=int(position_y_picker.get()))
    return watermark


def add_watermark_to_image(img_panel, watermark_config: wt.Watermark):
    # check if there is an image on the right canvas
    if hasattr(img_panel, "image_path"):
        img = Image.open(img_panel.image_path)
        img = img.resize((800, 800))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(watermark_config.font, watermark_config.fontsize)
        text_position = (watermark_config.pos_x, watermark_config.pos_y)
        draw.text(text_position, watermark_config.text, watermark_config.color, font=font)

        img_tk = ImageTk.PhotoImage(img)
        img_panel.config(image=img_tk)
        img_panel.image = img_tk
        panel.pil_image = img


def save_watermarked_image(img_panel):
    if hasattr(img_panel, "pil_image"):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            # TODO: Implement logic for saving image in original quality, scale the watermark if needed etc.
            img_panel.pil_image.save(file_path)


### Layout
# TODO: Fix layout: grid is breaking apart
# TODO: Define some fix values to improve general UI eg. padding on individual controls
root = tk.Tk()
root.title("Watermarking App")
root.geometry("1200x800")

# Create the left column (settings)
left_frame = tk.Frame(root, width=300, height=800, bg=winconf.LEFT_COLUMN_BG)
left_frame.pack(side="left", fill="both")

# title label for the left column
settings_label = Label(left_frame, text="Watermark configuration", font=("Arial", 18))
settings_label.pack(pady=10)

# left column elements:
# Listbox
listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE, width=40, height=10)
listbox.pack(pady=5, padx=10)
listbox.bind('<<ListboxSelect>>', display_image)

# Button to load add, remove images
# grouped in a frame
button_holder_frame = tk.Frame(left_frame, bg=winconf.LEFT_COLUMN_BG)
button_holder_frame.pack(pady=10)

load_image_button = Button(button_holder_frame, text="Load Image",
                           command=lambda: add_image_to_list(listbox))
load_image_button.grid(row=0, column=0, padx=10)

remove_image_button = Button(button_holder_frame, text="Remove Image",
                             command=remove_image_from_list)
remove_image_button.grid(row=0, column=1, padx=10)

# Text configuration
text_settings_label = Label(left_frame, text="Edit Text", font=("Arial", 18))
text_settings_label.pack(pady=10)

text_configuration_frame = tk.Frame(left_frame, bg=winconf.LEFT_COLUMN_BG)
text_configuration_frame.pack(pady=10)

# text input and preview
text_input_label = Label(text_configuration_frame, text="Text", bg=winconf.LEFT_COLUMN_BG)
text_input_label.grid(row=0, column=0, padx=10)
text_input_field = tk.Entry(text_configuration_frame, width=30)
text_input_field.grid(row=0, column=1)
# Font
font_label = Label(text_configuration_frame, text="Font", bg=winconf.LEFT_COLUMN_BG)
font_label.grid(row=1, column=0)

# color picker
font_var = tk.StringVar()
# TODO: create config class for the fonts find other fonts that work
font_choices = {"arial.ttf", 'times.ttf'}
font_var.set('arial.ttf')  # set the default option
font_picker = ttk.Combobox(text_configuration_frame, textvariable=font_var, values=list(font_choices))
font_picker.grid(row=1, column=1)

# Color
color_label = Label(text_configuration_frame, text="Color", bg='lightgray')
color_label.grid(row=2, column=0)
# color picker
tk_var = tk.StringVar()
# TODO: refactor picker to use the values from the color enum
choices = {'red', 'green', 'yellow', 'black'}
tk_var.set('red')  # set the default option
color_picker = ttk.Combobox(text_configuration_frame, textvariable=tk_var, values=list(choices))
color_picker.grid(row=2, column=1)

# Font size
font_size_label = Label(text_configuration_frame, text="Font size", bg=winconf.LEFT_COLUMN_BG)
font_size_label.grid(row=3, column=0)
# font size picker
font_size_var = tk.IntVar()
font_size_var.set(12)  # set the default value
#   Create the Spinbox
font_size_picker = tk.Spinbox(text_configuration_frame, from_=1, to=72, textvariable=font_size_var, width=5)
font_size_picker.grid(row=3, column=1)

# Buttons (Tile) Single Pattern
tile_label = Label(text_configuration_frame, text="Tile", bg=winconf.LEFT_COLUMN_BG)
tile_label.grid(row=4, column=0)

# opacity
opacity_label = Label(text_configuration_frame, text="Opacity", bg=winconf.LEFT_COLUMN_BG)
opacity_label.grid(row=5, column=0)

# opacity picker
opacity_var = tk.IntVar()
# set the default value
#   Create the Spinbox
opacity_picker = tk.Spinbox(text_configuration_frame, from_=0, to=100, textvariable=opacity_var, width=5)
opacity_picker.grid(row=5, column=1)

# TODO: add rotation parameter control

# TODO: add pattern watermark control

# POSITION INPUT
# position input X
# TODO: enable position calculation relative to the image size, currently fixed to 800pxs
position_x_label = Label(text_configuration_frame, text="Position X", bg=winconf.LEFT_COLUMN_BG)
position_x_label.grid(row=6, column=0)
position_var = tk.IntVar()
position_var.set(400)
position_x_picker = tk.Spinbox(text_configuration_frame, from_=0, to=800, textvariable=position_var, width=5)
position_x_picker.grid(row=6, column=1)

position_y_label = Label(text_configuration_frame, text="Position Y", bg=winconf.LEFT_COLUMN_BG)
position_y_label.grid(row=7, column=0)

position_y_picker = tk.Spinbox(text_configuration_frame, from_=0, to=800, textvariable=position_var, width=5)
position_y_picker.grid(row=7, column=1)

# button add watermark
add_watermark_to_image_button = Button(text_configuration_frame, text="Add text",
                                       command=lambda: add_watermark_to_image(panel,
                                                                              build_watermark_configuration()))
add_watermark_to_image_button.grid(row=8, column=0, padx=10)

# save watermarked image
save_watermarked_image_button = Button(text_configuration_frame, text="Save image",
                                       command=lambda: save_watermarked_image(img_panel=panel))
save_watermarked_image_button.grid(row=8, column=1, padx=10)

# RIGHT PANEL
# Create the right column (image display)
right_frame = tk.Frame(root, width=800, height=800, bg='white')
right_frame.pack(side="right", fill="both", padx=10, pady=10)

# Add an image display panel in the right column
panel = Label(right_frame)
panel.pack()

# Start the Tkinter main loop
root.mainloop()
