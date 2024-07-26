import bpy  # type: ignore
import os
import zipfile
from bpy.props import StringProperty, FloatProperty, EnumProperty, BoolProperty  # type: ignore
from bpy_extras.io_utils import ImportHelper  # type: ignore
from .functions.cleanup import cleanup_default_objects
from .functions.apply_textures import apply_textures
from .functions.resize import resize_object
from .functions.turntable import setup_turntable_camera, add_lights
from .functions.utils import check_files_exist, get_subdirectory_path

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
    import_for: EnumProperty(  # type: ignore
        name="Import For",
        description="Select the configuration type",
        items=[
            ('DEFAULT', "Default", "Default configuration"),
            ('UNREAL', "Unreal", "Configure the model for Unreal Engine"),
            ('TURNTABLE', "Turntable", "Add a rotating camera for turntable animation")
        ],
        default='DEFAULT'
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

        if not check_files_exist(obj_path, texture_paths):
            return {'CANCELLED'}

        if self.rename_objects:
            self.rename_collection('Collection', 'Character')
        if self.remove_default_objects:
            cleanup_default_objects()

        result = apply_textures(obj_path, texture_paths, base_name, self.ior, self.import_for)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}

        if self.rename_objects:
            self.rename_imported_object(base_name)
        if self.import_for in ['UNREAL', 'TURNTABLE']:
            result = resize_object(scale=(0.054, 0.054, 0.054))
            if result == {'CANCELLED'}:
                return {'CANCELLED'}

        if self.import_for == 'TURNTABLE':
            setup_turntable_camera()
            add_lights()

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
