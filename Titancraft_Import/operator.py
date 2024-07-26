import bpy  # type: ignore
from bpy.props import StringProperty, FloatProperty, EnumProperty, BoolProperty  # type: ignore
from bpy_extras.io_utils import ImportHelper  # type: ignore
from .functions.cleanup import cleanup_default_objects
from .functions.apply_textures import apply_textures
from .functions.resize import resize_object
from .functions.turntable import setup_turntable_camera, add_lights
from .functions.utils import check_files_exist, get_subdirectory_path
from .functions.io import extract_zip, get_file_paths, rename_collection, rename_imported_object

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
        base_name, extract_to = extract_zip(self.filepath)
        obj_path, texture_paths = get_file_paths(base_name, extract_to)

        if not check_files_exist(obj_path, texture_paths):
            return {'CANCELLED'}

        if self.rename_objects:
            rename_collection('Collection', 'Character')
        if self.remove_default_objects:
            cleanup_default_objects()

        result = apply_textures(obj_path, texture_paths, base_name, self.ior, self.import_for)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}

        if self.rename_objects:
            rename_imported_object(base_name)
        if self.import_for in ['UNREAL', 'TURNTABLE']:
            result = resize_object(scale=(0.054, 0.054, 0.054))
            if result == {'CANCELLED'}:
                return {'CANCELLED'}

        if self.import_for == 'TURNTABLE':
            setup_turntable_camera()
            add_lights()

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
