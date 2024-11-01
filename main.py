import tkinter as tk
from tkinter import Label, Entry, Button, Toplevel, StringVar, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Define the path to your image file
image_path = r"C:\Users\niksi\Downloads\as-ssd-bench kingston 256MD202 SC 31.10.2024 13-40-47 (1).png"

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Load the image
image = Image.open(image_path)
image_tk = ImageTk.PhotoImage(image)

# Create a label widget to display the image
label = Label(root, image=image_tk)
label.pack(pady=10)  # Add vertical padding around the image

# Center the main window on the screen
window_width = 800  # Set the desired width for the main window
window_height = 600  # Set the desired height for the main window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


def add_watermark_text():
    # Create a new window for entering watermark text
    watermark_window = Toplevel(root)
    watermark_window.title("Enter Watermark Text")

    # Center the watermark window on the image
    watermark_window.update_idletasks()  # Update the window size
    watermark_width = 300
    watermark_height = 300  # Increased height to accommodate new elements
    watermark_x = int(root.winfo_x() + (root.winfo_width() / 2) - (watermark_width / 2))
    watermark_y = int(root.winfo_y() + (root.winfo_height() / 2) - (watermark_height / 2))
    watermark_window.geometry(f"{watermark_width}x{watermark_height}+{watermark_x}+{watermark_y}")

    # Create a label for the watermark text input
    instruction_label = Label(watermark_window, text="Write the text of your watermark:")
    instruction_label.pack(pady=(10, 0))  # Padding above the label

    # Create an entry widget to get the watermark text with padding
    entry = Entry(watermark_window, width=40, bd=2, relief="groove")  # Adding border and relief style
    entry.pack(padx=10, pady=10)  # Add horizontal and vertical padding

    # Create a variable to store the selected position
    position_var = StringVar(value="center")  # Default position

    # Create a frame for the radio buttons
    positions_frame = tk.Frame(watermark_window)
    positions_frame.pack(pady=10)

    tk.Label(positions_frame, text="Select Watermark Position:").grid(row=0, columnspan=2)

    # Create radio buttons for watermark position selection in a grid layout
    tk.Radiobutton(positions_frame, text="Center", variable=position_var, value="center").grid(row=1, column=0,
                                                                                               sticky="w")
    tk.Radiobutton(positions_frame, text="Top Left", variable=position_var, value="top_left").grid(row=1, column=1,
                                                                                                   sticky="w")
    tk.Radiobutton(positions_frame, text="Top Right", variable=position_var, value="top_right").grid(row=2, column=0,
                                                                                                     sticky="w")
    tk.Radiobutton(positions_frame, text="Bottom Left", variable=position_var, value="bottom_left").grid(row=2,
                                                                                                         column=1,
                                                                                                         sticky="w")
    tk.Radiobutton(positions_frame, text="Bottom Right", variable=position_var, value="bottom_right").grid(row=3,
                                                                                                           column=0,
                                                                                                           sticky="w")

    # Create a label for font size selection
    font_size_label = Label(watermark_window, text="Select Font Size:")
    font_size_label.pack(pady=(10, 0))

    # Create a dropdown menu for font sizes
    font_sizes = [20, 24, 28, 32, 36, 40]  # Define font sizes
    font_size_var = StringVar(value=36)  # Default font size
    font_size_combobox = ttk.Combobox(watermark_window, textvariable=font_size_var, values=font_sizes, state="readonly")
    font_size_combobox.pack(padx=10, pady=10)  # Add padding

    # Create a button to confirm the watermark text
    confirm_button = Button(watermark_window, text="Add Watermark",
                            command=lambda: add_watermark(entry.get(), position_var.get(), font_size_var.get(),
                                                          watermark_window))
    confirm_button.pack(pady=10)


def add_watermark(watermark_text, position, font_size, window):
    # Create a copy of the image to add the watermark
    watermarked_image = image.copy()
    draw = ImageDraw.Draw(watermarked_image)

    # Convert font_size to integer
    font_size = int(font_size)

    # You can customize the font and size here
    try:
        # You may need to adjust the font path based on your system
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate the bounding box of the text
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Set padding for the watermark
    padding = 10

    # Position the watermark based on the selected option
    if position == "center":
        x = (watermarked_image.width - text_width) // 2
        y = (watermarked_image.height - text_height) // 2
    elif position == "top_left":
        x = padding
        y = padding
    elif position == "top_right":
        x = watermarked_image.width - text_width - padding
        y = padding
    elif position == "bottom_left":
        x = padding
        y = watermarked_image.height - text_height - padding
    elif position == "bottom_right":
        x = watermarked_image.width - text_width - padding
        y = watermarked_image.height - text_height - padding

    # Add the watermark with 20% opacity
    watermark_color = (255, 255, 255, int(255 * 0.2))  # 20% opacity
    draw.text((x, y), watermark_text, fill=watermark_color, font=font)

    # Update the displayed image
    watermarked_image_tk = ImageTk.PhotoImage(watermarked_image)
    label.config(image=watermarked_image_tk)
    label.image = watermarked_image_tk  # Keep a reference to avoid garbage collection

    # Close the watermark entry window
    window.destroy()


# Create a button to open the watermark text entry window
button = Button(root, text="Add Watermark", command=add_watermark_text, padx=10, pady=5)
button.pack(pady=(10, 20))  # Add padding above and below the button

# Run the application
root.mainloop()
