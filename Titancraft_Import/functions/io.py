import bpy  # type: ignore
import os
import zipfile

def extract_zip(filepath):
    extract_to = bpy.app.tempdir
    print(f"Extracting to: {extract_to}")
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    zip_filename = os.path.splitext(os.path.basename(filepath))[0]
    base_name = '_'.join(zip_filename.split('_')[:-1])  # Join all parts except the last one
    print(f"Base name: {base_name}")

    return base_name, extract_to

def get_file_paths(base_name, extract_to):
    obj_path = os.path.join(extract_to, f"{base_name}.obj")
    texture_paths = {
        'ao': os.path.join(extract_to, f"{base_name}_ao.png"),
        'color': os.path.join(extract_to, f"{base_name}_color.png"),
        'metallic': os.path.join(extract_to, f"{base_name}_metallic.png"),
        'normals': os.path.join(extract_to, f"{base_name}_normals.png"),
        'roughness': os.path.join(extract_to, f"{base_name}_roughness.png")
    }

    if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
        subdirectory_path = get_subdirectory_path(extract_to)
        if subdirectory_path:
            obj_path = os.path.join(subdirectory_path, f"{base_name}.obj")
            texture_paths = {
                'ao': os.path.join(subdirectory_path, f"{base_name}_ao.png"),
                'color': os.path.join(subdirectory_path, f"{base_name}_color.png"),
                'metallic': os.path.join(subdirectory_path, f"{base_name}_metallic.png"),
                'normals': os.path.join(subdirectory_path, f"{base_name}_normals.png"),
                'roughness': os.path.join(subdirectory_path, f"{base_name}_roughness.png")
            }

    return obj_path, texture_paths

def rename_collection(old_name, new_name):
    if old_name in bpy.data.collections:
        bpy.data.collections[old_name].name = new_name
        print(f"Renamed collection '{old_name}' to '{new_name}'.")

def rename_imported_object(new_name):
    imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if imported_objects:
        imported_objects[-1].name = new_name
        print(f"Renamed imported object to '{new_name}'.")
