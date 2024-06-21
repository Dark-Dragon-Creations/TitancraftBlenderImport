import bpy  # type: ignore

def resize_object(scale=(1, 1, 1)):
    print("Resizing object...")

    # Ensure the object is selected
    obj = bpy.context.view_layer.objects.active
    if not obj:
        print("No active object to resize.")
        return {'CANCELLED'}
    
    obj.scale = scale
    bpy.context.view_layer.update()  # Update the view layer

    return {'FINISHED'}
