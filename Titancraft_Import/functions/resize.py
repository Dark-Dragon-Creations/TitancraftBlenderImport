import bpy  # type: ignore
from .logging_utils import get_logger, log_operation_start, log_operation_success, log_operation_error

def resize_object(scale=(1, 1, 1), logger=None):
    """Resize the active object to the specified scale."""
    if logger is None:
        logger = get_logger()
    
    log_operation_start("object resizing", logger)

    # Ensure the object is selected
    obj = bpy.context.view_layer.objects.active
    if not obj:
        log_operation_error("object resizing", "No active object to resize", logger)
        return {'CANCELLED'}
    
    obj.scale = scale
    bpy.context.view_layer.update()  # Update the view layer
    
    logger.info(f"Resized object to scale: {scale}")
    log_operation_success("object resizing", logger)
    return {'FINISHED'}
