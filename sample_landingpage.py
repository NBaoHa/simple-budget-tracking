import tkinter as tk
from tkinter import ttk

# Create the root window
root = tk.Tk()
root.title("Modern Landing Page")
root.geometry("800x600")

# Create a frame for the header
header_frame = ttk.Frame(root, height=100)
header_frame.pack(side='top', fill='x')

# Create a label for the header
header_label = ttk.Label(header_frame, text="Welcome to Our Modern Landing Page!", font=("Arial", 16))
header_label.pack(side='top', pady=10)

# Create a frame for the main content
main_frame = ttk.Frame(root)
main_frame.pack(side='top', fill='both', expand=True)

# Create a label for the main content
main_label = ttk.Label(main_frame, text="Here is some main content for our landing page. You can use this space to showcase your product or service, or to provide information about your company.", font=("Arial", 14), wraplength=700)
main_label.pack(side='top', pady=10)

# Create a frame for the footer
footer_frame = ttk.Frame(root, height=50)
footer_frame.pack(side='bottom', fill='x')

# Create a label for the footer
footer_label = ttk.Label(footer_frame, text="Copyright 2022. All Rights Reserved.", font=("Arial", 12))
footer_label.pack(side='top', pady=10)

# Run the Tkinter event loop
root.mainloop()
