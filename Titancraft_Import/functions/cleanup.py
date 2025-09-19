import bpy  # type: ignore
from .constants import FileConstants

def cleanup_default_objects():
    bpy.ops.object.select_all(action='DESELECT')
    # Check and select objects if they exist
    for obj_name in FileConstants.DEFAULT_OBJECTS:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].select_set(True)
    bpy.ops.object.delete()
