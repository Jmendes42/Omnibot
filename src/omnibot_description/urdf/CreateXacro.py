
import glob
import os
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))

# Remove old meshes dir and create new one
destination_directory = current_directory + "/../meshes"

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

    # Define the old and new lines for specific replacements
    target_line = '<robot name="omnibot">'
    new_line = '<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="omnibot">'

    # Define the include line to add after replacing target_line
    include_line = '<xacro:include filename="$(find omnibot_description)/urdf/omnibot_gazebo.xacro"/>\n'
    include_line2 = '<xacro:include filename="$(find omnibot_description)/urdf/omnibot_ros2_control.xacro"/>\n\n'

    # Create a list to hold the modified lines
    modified_lines = []

    # Iterate over the original lines and apply replacements
    for line in lines:
        # Replace target line and add the include line right after it
        if line.strip() == target_line:
            modified_lines.append(new_line + '\n')  # Replace target line
            modified_lines.append(include_line)  # Add the new include line
            modified_lines.append(include_line2)  # Add the new include line
        else:
            # Perform other replacements
            line = line.replace("revolute", "continuous")
            line = line.replace("package://omnibot_description/urdf/", "package://omnibot_description/meshes/")
            line = line.replace("base_link", "base_footprint")
            line = line.replace("\"roller\"", "\"roller_1\"")
            modified_lines.append(line)

    # Add an XML declaration as the first line
    first_line = '<?xml version="1.0"?>\n\n'

    # Write the modified content back to the file
    with open(new_urdf_path, 'w') as file:
        file.write(first_line)
        file.writelines(modified_lines)

    print(f"Replaced target lines and added a new first line to {new_urdf_filename}.")
else:
    print(f"{new_urdf_filename} file not found.")