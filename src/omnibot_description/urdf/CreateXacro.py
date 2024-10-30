
import glob
import os
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))

# Remove old meshes dir and create new one
destination_directory = current_directory + "/meshes"

if os.path.exists(destination_directory):
    shutil.rmtree(destination_directory)

os.makedirs(destination_directory)

# Move .stl files to meshes/
stl_files = glob.glob(os.path.join(current_directory, "*.stl"))
for stl_file in stl_files:
    shutil.move(stl_file, destination_directory)
print(f"Moved {len(stl_files)} .stl files to {destination_directory}.")

# Delete unwanted files
part_files = glob.glob(os.path.join(current_directory, "*.part"), recursive=False)
for part_file in part_files:
    os.remove(part_file)
print(f"Deleted {len(part_files)} .part files from {current_directory}.")

# Rename urdf file
urdf_file = os.path.join(current_directory, "robot.urdf")
new_urdf_filename = "robot.urdf.xacro"
new_urdf_path = os.path.join(current_directory, new_urdf_filename)

if os.path.exists(urdf_file):
    os.rename(urdf_file, new_urdf_path)
    print(f"Renamed {urdf_file} to {new_urdf_filename}.")
else:
    print("robot.urdf file not found in the source directory.")

# Replace items in .xacro file
if os.path.exists(new_urdf_path):
    with open(new_urdf_path, 'r') as file:
        lines = file.readlines()

    target_line = '<robot name="omnibot">'
    new_line = '<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="omnibot">'
    modified_lines = [new_line + '\n' if line.strip() == target_line else line for line in lines]
    modified_lines = [line.replace("revolute", "continuous") for line in modified_lines]
    modified_lines = [line.replace("package:///", "package://omnibot_description/meshes/") for line in modified_lines]

    first_line = '<?xml version="1.0"?>\n\n'

    with open(new_urdf_path, 'w') as file:
        file.write(first_line)
        file.writelines(modified_lines)

    print(f"Replaced the target line and added a new first line to {new_urdf_filename}.")
else:
    print(f"{new_urdf_filename} file not found.")