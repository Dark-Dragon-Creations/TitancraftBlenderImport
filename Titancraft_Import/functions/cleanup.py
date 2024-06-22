import bpy  # type: ignore

def cleanup_default_objects():
    bpy.ops.object.select_all(action='DESELECT')
    # Check and select objects if they exist
    for obj_name in ['Cube', 'Light', 'Camera']:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].select_set(True)
    bpy.ops.object.delete()
