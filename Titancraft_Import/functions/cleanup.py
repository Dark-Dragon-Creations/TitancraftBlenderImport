import bpy  # type: ignore

def cleanup_default_objects():
    print("Cleaning up default objects...")
    bpy.ops.object.select_all(action='DESELECT')
    
    if 'Cube' in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()
    
    if 'Camera' in bpy.data.objects:
        bpy.data.objects['Camera'].select_set(True)
        bpy.ops.object.delete()
    
    if 'Light' in bpy.data.objects:
        bpy.data.objects['Light'].select_set(True)
        bpy.ops.object.delete()
