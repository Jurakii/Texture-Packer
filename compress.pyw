import os
import zipfile
import threading
from javax.swing import (JFrame, JButton, JLabel, JTextField,
                         JComboBox, JProgressBar, JOptionPane, JFileChooser, ImageIcon)
from java.awt import GridBagLayout, GridBagConstraints, Insets
from javax.imageio import ImageIO
from java.io import File

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

def compress_folder(source_folder, destination_folder, zip_filename):
    try:
        total_files = sum(1 for root, dirs, files in os.walk(source_folder) for file in files)
        progress_bar.setMaximum(total_files)
        progress_bar.setValue(0)

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            progress = 0
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, source_folder)
                    zipf.write(file_path, archive_name)
                    progress += 1
                    progress_bar.setValue(progress)

        JOptionPane.showMessageDialog(frame, "Successfully compressed files to " + zip_filename)

    except Exception as e:
        JOptionPane.showMessageDialog(frame, "Error: " + str(e))

    finally:
        compress_button.setEnabled(True)

def set_destination_and_compress(event):
    selected_folder_value = source_paths_combobox.getSelectedItem()
    selected_destination_value = destination_paths_combobox.getSelectedItem()
    if selected_folder_value and selected_destination_value:
        zip_filename = os.path.join(selected_destination_value, 'Textures.zip')
        compress_button.setEnabled(False)
        threading.Thread(target=compress_folder, args=(selected_folder_value, selected_destination_value, zip_filename)).start()

def add_file_path(combobox):
    file_chooser = JFileChooser()
    file_chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
    result = file_chooser.showOpenDialog(frame)
    if result == JFileChooser.APPROVE_OPTION:
        selected_folder = file_chooser.getSelectedFile().getPath()
        combobox.addItem(selected_folder)

# Search for PNG file in the directory and set it as app icon
def set_icon_from_png(directory):
    for file_name in os.listdir(directory):
        if file_name.lower().endswith('.png'):
            icon_path = os.path.join(directory, file_name)
            icon_image = ImageIO.read(File(icon_path))
            frame.setIconImage(icon_image)
            break

# Create the main window
frame = JFrame("Texture Packer")
frame.setSize(425, 350)
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
frame.setLayout(GridBagLayout())

# Set app icon from PNG file in the directory
icon_directory = os.path.join(script_dir, "_internal")
set_icon_from_png(icon_directory)

# Create labels and comboboxes
source_label = JLabel("Source Folder:")
destination_label = JLabel("Destination Folder:")
source_paths_combobox = JComboBox(["Select a source folder"])
destination_paths_combobox = JComboBox(["Select a destination folder"])

# Create buttons
new_button = JButton("New Source", actionPerformed=lambda event: add_file_path(source_paths_combobox))
new_button2 = JButton("New Destination", actionPerformed=lambda event: add_file_path(destination_paths_combobox))
compress_button = JButton("Save and Compress", actionPerformed=set_destination_and_compress)

# Create and configure the progress bar
progress_bar = JProgressBar(0, 100)

# Add components to the main window
constraints = GridBagConstraints()
constraints.fill = GridBagConstraints.HORIZONTAL
constraints.weightx = 1
constraints.gridx = 0
constraints.gridy = 0
constraints.insets = Insets(10, 10, 10, 10)  # Add top and bottom margins
frame.add(new_button, constraints)

constraints.gridx = 1
frame.add(new_button2, constraints)

constraints.gridy = 1
constraints.gridx = 0
frame.add(source_label, constraints)

constraints.gridx = 1
frame.add(destination_label, constraints)

constraints.gridy = 2
constraints.gridwidth = 1
frame.add(destination_paths_combobox, constraints)

constraints.gridx = 0
frame.add(source_paths_combobox, constraints)

constraints.gridwidth = 2
constraints.gridy = 3
constraints.insets = Insets(20, 10, 0, 10)  # Add only bottom margin
frame.add(compress_button, constraints)

constraints.gridy = 4
frame.add(progress_bar, constraints)

frame.setVisible(True)
