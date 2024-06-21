import json
import os
import sys
import zipfile
import subprocess
import shutil

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def clear_output_folder(output_folder):
    for root, dirs, files in os.walk(output_folder):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                shutil.rmtree(dir_path)
            except Exception as e:
                print(f'Failed to delete {dir_path}. Reason: {e}')

def main():
    input_folder = "Input"
    output_folder = "Output"
    config_file = "config.json"
    
    # Ensure Input and Output folders exist
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load configuration
    if not os.path.exists(config_file):
        print(f"No configuration file found: {config_file}")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    export_obj = config.get('export_obj', False)
    blender_executable = config.get('blender_executable', '')
    launch_blender = config.get('launch_blender', False)
    scale_for_ue = config.get('scale_for_ue', False)
    ior = config.get('ior', 1.05)
    x_offset = config.get('x_offset', 300)
    y_offset = config.get('y_offset', 400)
    debug_mode = config.get('debug', False)
    cleanup_objects = config.get('cleanup_objects', True)
    apply_textures = config.get('apply_textures', True)
    resize_object = config.get('resize_object', True)

    if not blender_executable:
        print("Blender executable path is not configured.")
        return
    
    # Clear output folder if debug mode is enabled
    if debug_mode:
        clear_output_folder(output_folder)
    
    # Find the zip file in the input folder
    zip_file = None
    for file in os.listdir(input_folder):
        if file.endswith(".zip"):
            zip_file = file
            zip_file_path = os.path.join(input_folder, zip_file)
            break
    
    if not zip_file:
        print("No zip file found in the input folder.")
        return
    
    # Determine the base name from the zip file name
    base_name = zip_file.split('_')[0]
    
    # Set paths
    extract_to = os.path.join(input_folder, base_name)
    os.makedirs(extract_to, exist_ok=True)
    
    # Unzip the file
    unzip_file(zip_file_path, extract_to)
    
    # File paths
    obj_path = os.path.join(extract_to, f"{base_name}.obj")
    texture_paths = {
        'diffuse': os.path.join(extract_to, f"{base_name} Albedo.png"),
        'normal': os.path.join(extract_to, f"{base_name} Normals.png"),
        'metallic': os.path.join(extract_to, f"{base_name} Metallic AO Roughness.png")
    }

    # Debug: Print the paths to ensure they are correct
    print(f"OBJ file path: {obj_path}")
    print(f"Diffuse texture path: {texture_paths['diffuse']}")
    print(f"Normal texture path: {texture_paths['normal']}")
    print(f"Metallic texture path: {texture_paths['metallic']}")

    # Prepare the common arguments for Blender scripts
    common_args = [
        obj_path,
        texture_paths['diffuse'],
        texture_paths['normal'],
        texture_paths['metallic'],
        output_folder,
        base_name,
        str(export_obj),
        str(launch_blender),
        str(scale_for_ue),
        str(ior),
        str(x_offset),
        str(y_offset)
    ]

    # Define the scripts to run based on configuration
    scripts_to_run = []
    if cleanup_objects:
        scripts_to_run.append('cleanup.py')
    if apply_textures:
        scripts_to_run.append('apply_textures.py')
    if resize_object:
        scripts_to_run.append('resize.py')

    # Run the consolidated Blender script with arguments
    print(f"Running consolidated Blender script: blender_pipeline.py")
    command = [blender_executable, '--background', '--python', 'blender_pipeline.py', '--'] + common_args
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"Error running Blender pipeline script")
        return

    # If configured to launch Blender, do so
    if launch_blender:
        output_file_path = os.path.join(output_folder, f"{base_name}.blend")
        print(f"Launching Blender with file: {output_file_path}")
        subprocess.run([blender_executable, output_file_path])

if __name__ == "__main__":
    main()
