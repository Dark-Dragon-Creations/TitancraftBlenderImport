import bpy  # type: ignore

def resize_object():
    print("Resizing object...")
    obj = bpy.context.selected_objects[0]
    obj.scale = (0.054, 0.054, 0.054)
