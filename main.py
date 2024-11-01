import tkinter as tk
from tkinter import Label, Entry, Button, Toplevel, StringVar, ttk, filedialog, Scrollbar, Canvas, Frame
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


class ImageWatermarker:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        # Initialize main components and variables
        self.image = None
        self.image_tk = None
        self.setup_ui()
        self.center_window(800, 600)

        # Bind mouse wheel event for scrolling
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def setup_ui(self):
        # Frame for image and vertical scrollbar
        image_frame = Frame(self.root)
        image_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas with vertical scrollbar
        self.canvas = Canvas(image_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        self.v_scrollbar = Scrollbar(image_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar placed under the image, outside of the image frame
        h_scrollbar = Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.pack(fill=tk.X)

        # Configure canvas scroll command for both scrollbars
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Container for the image
        self.image_container = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_container, anchor="nw")

        # Initial message in the container
        self.initial_message = Label(self.image_container, text="Load an image using the open file button",
                                     font=("Arial", 16))
        self.initial_message.pack(pady=10)

        # Label to display images
        self.label = Label(self.image_container)
        self.label.pack()

        # Frame for buttons, packed with fill on the x-axis
        button_frame = Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=(10, 20), fill=tk.X)

        # Buttons for opening image, adding watermark, and saving in order
        button_width = 15  # Fixed width for buttons
        button_spacing = 5  # Space between buttons

        # Button for saving the image
        save_button = Button(button_frame, text="Save", command=self.save_image, padx=10, pady=5, width=button_width)
        save_button.pack(side=tk.RIGHT, padx=(button_spacing, 20))  # Added padding to the right edge

        # Button for adding watermark
        watermark_button = Button(button_frame, text="Add Watermark", command=self.add_watermark_text, padx=10, pady=5, width=button_width)
        watermark_button.pack(side=tk.RIGHT, padx=(button_spacing, 0))

        # Button for opening image
        open_button = Button(button_frame, text="Open Image", command=self.open_image, padx=10, pady=5, width=button_width)
        open_button.pack(side=tk.RIGHT, padx=(button_spacing, 0))

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_image(self):
        # Open file dialog and load the selected image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.load_image(file_path)

    def load_image(self, image_path):
        # Load the image and resize if necessary
        self.image = Image.open(image_path)
        self.resize_image_if_needed()

        # Convert image to Tkinter-compatible format and update the label
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label.config(image=self.image_tk)
        self.label.image = self.image_tk

        # Remove the initial message if it exists
        if self.initial_message:
            self.initial_message.destroy()
            self.initial_message = None

        # Update the scroll region to fit the image exactly
        self.canvas.update_idletasks()  # Ensure canvas is updated
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Save the original image filename for saving later
        self.original_filename = os.path.basename(image_path)

    def resize_image_if_needed(self):
        # Resize the image if it's too large for the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        max_width, max_height = int(screen_width * 0.8), int(screen_height * 0.8)
        if self.image.width > max_width or self.image.height > max_height:
            self.image.thumbnail((max_width, max_height))

    def add_watermark_text(self):
        # Open a new window to input watermark text and options
        watermark_window = Toplevel(self.root)
        watermark_window.title("Enter Watermark Text")
        self.center_popup(watermark_window, 300, 300)

        # Input fields and options for watermark text, position, and size
        Label(watermark_window, text="Write the text of your watermark:").pack(pady=(10, 0))
        entry = Entry(watermark_window, width=40, bd=2, relief="groove")
        entry.pack(padx=10, pady=10)

        # Position selection radio buttons
        position_var = StringVar(value="center")
        positions_frame = Frame(watermark_window)
        positions_frame.pack(pady=10)
        Label(positions_frame, text="Select Watermark Position:").grid(row=0, columnspan=2)
        positions = ["Center", "Top Left", "Top Right", "Bottom Left", "Bottom Right"]
        for i, pos in enumerate(positions):
            row, col = divmod(i, 2)
            tk.Radiobutton(positions_frame, text=pos, variable=position_var, value=pos.lower().replace(" ", "_")).grid(
                row=row + 1, column=col, sticky="w")

        # Font size dropdown
        Label(watermark_window, text="Select Font Size:").pack(pady=(10, 0))
        font_size_var = StringVar(value=36)
        ttk.Combobox(watermark_window, textvariable=font_size_var, values=[20, 24, 28, 32, 36, 40],
                     state="readonly").pack(padx=10, pady=10)

        # Confirm button to add watermark
        confirm_button = Button(watermark_window, text="Add Watermark",
                                command=lambda: self.add_watermark(entry.get(), position_var.get(), font_size_var.get(),
                                                                   watermark_window))
        confirm_button.pack(pady=10)

    def add_watermark(self, text, position, font_size, window):
        # Create a new image with the watermark
        self.watermarked_image = self.image.convert("RGBA")
        watermark_layer = Image.new("RGBA", self.watermarked_image.size)

        draw = ImageDraw.Draw(watermark_layer)

        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", int(font_size))
        except IOError:
            font = ImageFont.load_default()

        # Get text bounding box and calculate position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        padding = 10

        # Determine coordinates based on the position
        positions = {
            "center": ((self.watermarked_image.width - text_width) // 2, (self.watermarked_image.height - text_height) // 2),
            "top_left": (padding, padding),
            "top_right": (self.watermarked_image.width - text_width - padding, padding),
            "bottom_left": (padding, self.watermarked_image.height - text_height - padding),
            "bottom_right": (
                self.watermarked_image.width - text_width - padding, self.watermarked_image.height - text_height - padding)
        }
        x, y = positions.get(position, positions["center"])

        # Draw watermark text with transparency
        watermark_color = (255, 255, 255, 128)  # Set transparency for a more subtle effect
        draw.text((x, y), text, fill=watermark_color, font=font)

        # Merge watermark layer with original image
        self.watermarked_image = Image.alpha_composite(self.watermarked_image, watermark_layer)

        # Convert back to RGB and update the displayed image
        self.image_tk = ImageTk.PhotoImage(self.watermarked_image.convert("RGB"))  # Update to RGB before displaying
        self.label.config(image=self.image_tk)
        self.label.image = self.image_tk
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Close watermark window
        window.destroy()

    def save_image(self):
        # Open file dialog to save the image with a watermark
        if not hasattr(self, 'watermarked_image'):
            tk.messagebox.showerror("Error", "No watermarked image to save.")
            return
        default_filename = self.original_filename.replace(".", "_watermark.")
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 initialfile=default_filename,
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"),
                                                            ("All files", "*.*")])
        if save_path:
            self.watermarked_image.convert("RGB").save(save_path)  # Save as RGB format

    def center_popup(self, popup, width, height):
        # Center a popup window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def on_mouse_wheel(self, event):
        # Scroll the canvas with the mouse wheel
        self.canvas.yview_scroll(int(-1 * (event.delta // 120)), "units")


# Main application start
root = tk.Tk()
app = ImageWatermarker(root)
root.mainloop()
