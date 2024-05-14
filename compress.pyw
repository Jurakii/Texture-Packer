import os
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import threading

def compress_folder(source_folder, destination_folder, zip_filename, progress_bar, compress_button):
    try:
        total_files = sum(1 for root, dirs, files in os.walk(source_folder) for file in files)
        progress_bar['maximum'] = total_files
        progress = 0

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, source_folder)
                    zipf.write(file_path, archive_name)
                    progress += 1
                    progress_bar['value'] = progress
        print(f'Successfully compressed files to {zip_filename}')

    except Exception as e:
        print(f'Error: {str(e)}')

    finally:
        compress_button.config(state='normal')

# Function to add a new file path to the Combobox and save it to the text file
def add_file_path():
    new_path = filedialog.askdirectory()
    if new_path:
        source_paths_combobox['values'] += (new_path,)
        with open('_internal/file_paths.txt', 'a') as file:
            file.write(new_path + '\n')

# Function to add a new destination file path to the Combobox and save it to the text file
def add_file_path2():
    new_path = filedialog.askdirectory()
    if new_path:
        destination_paths_combobox['values'] += (new_path,)
        with open('_internal/destination_folder.txt', 'a') as file:
            file.write(new_path + '\n')

# Function to set the destination folder and trigger the compression
def set_destination_and_compress():
    selected_folder_value = source_paths_combobox.get()
    with open('_internal/destination_folder.txt', 'r') as dest_file:
        selected_destination_value = dest_file.read().strip()
    if selected_folder_value and selected_destination_value:
        # Create a folder to store the compressed file
        zip_filename = os.path.join(selected_destination_value, 'Textures.zip')

        # Create and configure the progress bar
        progress_bar = ttk.Progressbar(root, mode='determinate', length=200)
        progress_bar.grid(row=4, columnspan=2, pady=10)

        # Disable the "Save and Compress" button during compression
        compress_button['state'] = 'disabled'

        # Start a new thread for compression
        threading.Thread(target=compress_folder, args=(selected_folder_value, selected_destination_value, zip_filename, progress_bar, compress_button)).start()

# Create the main window with a themed tkinter
root = ThemedTk(theme="arc")  # You can change "arc" to other themes

root.title("Texture Packer")
root.geometry("325x250")  # Larger window to accommodate the progress bar
# root.iconbitmap("icon.ico")
root.config(bg="#26242f") 

# Create a Combobox for source file paths with a larger font
source_paths_combobox = ttk.Combobox(root, values=["Select a source folder"], font=("Arial", 14))
source_paths_combobox.set("Select a source folder")

# Load existing source file paths
with open('_internal/file_paths.txt', 'r') as file:
    paths = [line.strip() for line in file]
    source_paths_combobox['values'] += tuple(paths)

# Create a Combobox for destination file paths with a larger font
destination_paths_combobox = ttk.Combobox(root, values=["Select a destination folder"], font=("Arial", 14))
destination_paths_combobox.set("Select a destination folder")

# Load existing destination file paths
with open('_internal/destination_folder.txt', 'r') as dest_file:
    dest_folder = dest_file.read().strip()
    destination_paths_combobox['values'] += (dest_folder,)

# Create a frame to center the buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=20)   # Use grid for better control

# Create the buttons with a larger font
new_button = ttk.Button(button_frame, text="New Source", command=add_file_path, style="TButton", width=20)
new_button2 = ttk.Button(button_frame, text="New Destination", command=add_file_path2, style="TButton", width=20)

# Use grid to center the buttons
new_button.grid(row=0, column=0, padx=10)  # Larger horizontal spacing
new_button2.grid(row=0, column=1, padx=10)  # Position the second button in the same row but in the second column

source_paths_combobox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
destination_paths_combobox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create the "Save and Compress" button
compress_button = ttk.Button(root, text="Save and Compress", command=set_destination_and_compress, style="TButton", width=20)
compress_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the main application loop
root.mainloop()
