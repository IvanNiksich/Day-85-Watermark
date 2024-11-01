import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Define the path to your image file
image_path = r"C:\Users\niksi\Downloads\solar_inverter_2.jpg"

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Load the image
image = Image.open(image_path)
image_tk = ImageTk.PhotoImage(image)

# Create a label widget to display the image
label = Label(root, image=image_tk)
label.pack()

# Run the application
root.mainloop()
