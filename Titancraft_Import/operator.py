import bpy  # type: ignore
import os
import zipfile
from bpy.props import StringProperty, FloatProperty, BoolProperty  # type: ignore
from bpy_extras.io_utils import ImportHelper  # type: ignore
from .functions.cleanup import cleanup_default_objects
from .functions.apply_textures import apply_textures
from .functions.resize import resize_object

class ImportApplyTexturesOperator(bpy.types.Operator, ImportHelper):  # type: ignore
    bl_idname = "titancraft_import.zip"
    bl_label = "Titancraft Import"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".zip"
    filter_glob: StringProperty(default="*.zip", options={'HIDDEN'})  # type: ignore
    ior: FloatProperty(  # type: ignore
        name="IOR",
        description="Index of Refraction for the material",
        default=1.05,
    )
    configure_for_unreal: BoolProperty(  # type: ignore
        name="Configure for Unreal",
        description="Configure the model for Unreal Engine",
        default=False,
    )
    remove_default_objects: BoolProperty(  # type: ignore
        name="Remove Default Objects",
        description="Remove the default camera, cube, and light",
        default=True,
    )
    rename_objects: BoolProperty(  # type: ignore
        name="Rename Objects",
        description="Rename the Collection and imported object",
        default=True,
    )

    def execute(self, context):
        base_name, extract_to = self.extract_zip()
        obj_path, texture_paths = self.get_file_paths(base_name, extract_to)

        if not self.check_files_exist(obj_path, texture_paths):
            return {'CANCELLED'}

        if self.rename_objects:
            self.rename_collection('Collection', 'Character')
        if self.remove_default_objects:
            cleanup_default_objects()

        result = apply_textures(obj_path, texture_paths, base_name, self.ior, self.configure_for_unreal)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}

        if self.rename_objects:
            self.rename_imported_object(base_name)
        if self.configure_for_unreal:
            result = resize_object(scale=(0.054, 0.054, 0.054))
            if result == {'CANCELLED'}:
                return {'CANCELLED'}

        return {'FINISHED'}

    def extract_zip(self):
        extract_to = bpy.app.tempdir
        print(f"Extracting to: {extract_to}")
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        zip_filename = os.path.splitext(os.path.basename(self.filepath))[0]
        base_name = '_'.join(zip_filename.split('_')[:-1])  # Join all parts except the last one
        print(f"Base name: {base_name}")

        return base_name, extract_to

    def get_file_paths(self, base_name, extract_to):
        obj_path = os.path.join(extract_to, f"{base_name}.obj")
        texture_paths = {
            'diffuse': os.path.join(extract_to, f"{base_name} Albedo.png"),
            'normal': os.path.join(extract_to, f"{base_name} Normals.png"),
            'metallic': os.path.join(extract_to, f"{base_name} Metallic AO Roughness.png")
        }

        if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
            # Try without base name
            obj_path = os.path.join(extract_to, "model.obj")
            texture_paths = {
                'diffuse': os.path.join(extract_to, "Albedo.png"),
                'normal': os.path.join(extract_to, "Normals.png"),
                'metallic': os.path.join(extract_to, "Metallic AO Roughness.png")
            }

            if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
                # Try with the new naming convention
                obj_path = os.path.join(extract_to, "model.obj")
                texture_paths = {
                    'diffuse': os.path.join(extract_to, "albedo.png"),
                    'normal': os.path.join(extract_to, "normals.png"),
                    'metallic': os.path.join(extract_to, "metallic_ao_roughness.png")
                }

                # Check again if files exist in subdirectory
                if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
                    subdirectory_path = self.get_subdirectory_path(extract_to)
                    if subdirectory_path:
                        obj_path = os.path.join(subdirectory_path, f"{base_name}.obj")
                        texture_paths = {
                            'diffuse': os.path.join(subdirectory_path, f"{base_name} Albedo.png"),
                            'normal': os.path.join(subdirectory_path, f"{base_name} Normals.png"),
                            'metallic': os.path.join(subdirectory_path, f"{base_name} Metallic AO Roughness.png")
                        }
                        if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
                            # Try without base name in subdirectory
                            obj_path = os.path.join(subdirectory_path, "model.obj")
                            texture_paths = {
                                'diffuse': os.path.join(subdirectory_path, "Albedo.png"),
                                'normal': os.path.join(subdirectory_path, "Normals.png"),
                                'metallic': os.path.join(subdirectory_path, "Metallic AO Roughness.png")
                            }
                            if not all(os.path.exists(path) for path in [obj_path, *texture_paths.values()]):
                                # Try with the new naming convention in subdirectory
                                obj_path = os.path.join(subdirectory_path, "model.obj")
                                texture_paths = {
                                    'diffuse': os.path.join(subdirectory_path, "albedo.png"),
                                    'normal': os.path.join(subdirectory_path, "normals.png"),
                                    'metallic': os.path.join(subdirectory_path, "metallic_ao_roughness.png")
                                }

        return obj_path, texture_paths

    def get_subdirectory_path(self, extract_to):
        subdirectories = [os.path.join(extract_to, d) for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]
        if len(subdirectories) == 1:
            subdirectory_path = subdirectories[0]
            print(f"Subdirectory path: {subdirectory_path}")
            return subdirectory_path
        return None

    def check_files_exist(self, obj_path, texture_paths):
        extracted_files = os.listdir(os.path.dirname(obj_path))
        print(f"Extracted files: {extracted_files}")

        print(f"OBJ file path: {obj_path}")
        print(f"Diffuse texture path: {texture_paths['diffuse']}")
        print(f"Normal texture path: {texture_paths['normal']}")
        print(f"Metallic texture path: {texture_paths['metallic']}")

        if not os.path.exists(obj_path):
            print(f"OBJ file not found: {obj_path}")
            return False
        for key, path in texture_paths.items():
            if not os.path.exists(path):
                print(f"Texture file not found: {path}")
                return False
        return True

    def rename_collection(self, old_name, new_name):
        if old_name in bpy.data.collections:
            bpy.data.collections[old_name].name = new_name
            print(f"Renamed collection '{old_name}' to '{new_name}'.")

    def rename_imported_object(self, new_name):
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if imported_objects:
            imported_objects[-1].name = new_name
            print(f"Renamed imported object to '{new_name}'.")

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
