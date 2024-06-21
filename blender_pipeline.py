import bpy  # type: ignore
import sys
import os
import shutil

# Ensure the script's directory is in the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from cleanup import cleanup_default_objects
from apply_textures import apply_textures
from resize import resize_object

def main():
    # Parse command line arguments
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

    obj_path = os.path.abspath(argv[0])
    texture_paths = {
        'diffuse': os.path.abspath(argv[1]),
        'normal': os.path.abspath(argv[2]),
        'metallic': os.path.abspath(argv[3])
    }
    output_folder = os.path.abspath(argv[4])
    base_name = argv[5]
    export_obj = argv[6].lower() == 'true'
    launch_blender = argv[7].lower() == 'true'
    scale_for_ue = argv[8].lower() == 'true'
    ior = float(argv[9])
    x_offset = int(argv[10])
    y_offset = int(argv[11])

    # Step 1: Cleanup default objects
    cleanup_default_objects()

    # Step 2: Apply textures
    apply_textures(obj_path, texture_paths, output_folder, base_name, ior, x_offset, y_offset)

    # Step 3: Resize object if needed
    if scale_for_ue:
        resize_object()

    # Step 4: Save the Blender file
    output_file_path = os.path.join(output_folder, f"{base_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_file_path)

    if export_obj:
        # Export the scene to OBJ format
        obj_output_path = os.path.join(output_folder, f"{base_name}.obj")
        bpy.ops.wm.obj_export(filepath=obj_output_path)

        # Copy texture files to the output folder
        for key, texture_path in texture_paths.items():
            shutil.copy(texture_path, output_folder)

    if launch_blender:
        # Launch Blender with the generated .blend file
        bpy.ops.wm.open_mainfile(filepath=output_file_path)

if __name__ == "__main__":
    main()
