import bpy # type: ignore
import os
import zipfile
from bpy.props import StringProperty, FloatProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from .functions.cleanup import cleanup_default_objects
from .functions.apply_textures import apply_textures
from .functions.resize import resize_object

class ImportApplyTexturesOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "titancraft_import.zip"
    bl_label = "Titancraft Import"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".zip"
    filter_glob: StringProperty(default="*.zip", options={'HIDDEN'})
    ior: FloatProperty(
        name="IOR",
        description="Index of Refraction for the material",
        default=1.05,
    )
    resize_for_ue: BoolProperty(
        name="Resize for UE",
        description="Resize the model for Unreal Engine",
        default=True,
    )

    def execute(self, context):
        # Unzip the file
        extract_to = bpy.app.tempdir
        print(f"Extracting to: {extract_to}")
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # Determine the base name from the zip file name
        zip_filename = os.path.splitext(os.path.basename(self.filepath))[0]
        base_name_parts = zip_filename.split('_')
        base_name = '_'.join(base_name_parts[:-1])  # Join all parts except the last one
        print(f"Base name: {base_name}")

        # Define the expected file paths
        obj_path = os.path.join(extract_to, f"{base_name}.obj")
        texture_paths = {
            'diffuse': os.path.join(extract_to, f"{base_name} Albedo.png"),
            'normal': os.path.join(extract_to, f"{base_name} Normals.png"),
            'metallic': os.path.join(extract_to, f"{base_name} Metallic AO Roughness.png")
        }

        # Check if files exist in the extraction directory
        if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
            # If files do not exist, check subdirectories
            subdirectories = [os.path.join(extract_to, d) for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]
            if len(subdirectories) == 1:
                subdirectory_path = subdirectories[0]
                print(f"Subdirectory path: {subdirectory_path}")
                obj_path = os.path.join(subdirectory_path, f"{base_name}.obj")
                texture_paths = {
                    'diffuse': os.path.join(subdirectory_path, f"{base_name} Albedo.png"),
                    'normal': os.path.join(subdirectory_path, f"{base_name} Normals.png"),
                    'metallic': os.path.join(subdirectory_path, f"{base_name} Metallic AO Roughness.png")
                }

        # List the contents of the extracted directory for debugging
        extracted_files = os.listdir(os.path.dirname(obj_path))
        print(f"Extracted files: {extracted_files}")

        # Debug: Print the paths to ensure they are correct
        print(f"OBJ file path: {obj_path}")
        print(f"Diffuse texture path: {texture_paths['diffuse']}")
        print(f"Normal texture path: {texture_paths['normal']}")
        print(f"Metallic texture path: {texture_paths['metallic']}")

        # Check if the extracted files exist
        if not os.path.exists(obj_path):
            print(f"OBJ file not found: {obj_path}")
            return {'CANCELLED'}
        for key, path in texture_paths.items():
            if not os.path.exists(path):
                print(f"Texture file not found: {path}")
                return {'CANCELLED'}

        # Step 1: Cleanup default objects
        cleanup_default_objects()

        # Step 2: Apply textures
        result = apply_textures(obj_path, texture_paths, base_name, self.ior)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}

        # Step 3: Resize object if the resize_for_ue property is set to True
        if self.resize_for_ue:
            result = resize_object(scale=(0.054, 0.054, 0.054))
            if result == {'CANCELLED'}:
                return {'CANCELLED'}

        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportApplyTexturesOperator.bl_idname, text="Titancraft (.zip)")

def register():
    bpy.utils.register_class(ImportApplyTexturesOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportApplyTexturesOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
