import os
import zipfile
import subprocess
import json

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

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

    if not blender_executable:
        print("Blender executable path is not configured.")
        return
    
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

    # Path to the Blender script
    blender_script = os.path.join(os.path.dirname(__file__), "blender_script.py")
    
    # Command to invoke Blender
    blender_command = [
        blender_executable,
        "--background",
        "--python", blender_script,
        "--", obj_path, texture_paths['diffuse'], texture_paths['normal'], texture_paths['metallic'], output_folder, base_name, str(export_obj), str(launch_blender), str(scale_for_ue)
    ]
    
    # Run the Blender command
    subprocess.run(blender_command)

    # Launch Blender with the generated .blend file if the flag is set
    if launch_blender:
        blend_file_path = os.path.join(output_folder, f"{base_name}.blend")
        subprocess.run([blender_executable, blend_file_path])

if __name__ == "__main__":
    main()
