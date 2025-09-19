import bpy  # type: ignore
from .constants import AnimationConstants, LightingConstants, CameraConstants, FileConstants

def setup_turntable_camera():
    # Add a camera
    bpy.ops.object.camera_add(location=CameraConstants.TURNTABLE_CAMERA_LOCATION, rotation=CameraConstants.TURNTABLE_CAMERA_ROTATION)
    camera = bpy.context.active_object
    camera.name = FileConstants.TURNTABLE_CAMERA_NAME

    # Add an empty object at the center of the model
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=CameraConstants.TURNTABLE_EMPTY_LOCATION)
    empty = bpy.context.active_object
    empty.name = FileConstants.TURNTABLE_EMPTY_NAME

    # Set the camera to look at the empty object
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = empty
    constraint.track_axis = CameraConstants.TRACK_AXIS
    constraint.up_axis = CameraConstants.UP_AXIS

    # Parent the camera to the empty object
    camera.parent = empty

    # Set up the animation for the empty object
    bpy.context.scene.frame_start = AnimationConstants.TURNTABLE_FRAME_START
    bpy.context.scene.frame_end = AnimationConstants.TURNTABLE_FRAME_END

    empty.rotation_euler = AnimationConstants.TURNTABLE_ROTATION_START
    empty.keyframe_insert(data_path="rotation_euler", frame=AnimationConstants.TURNTABLE_FRAME_START)
    empty.rotation_euler = AnimationConstants.TURNTABLE_ROTATION_END
    empty.keyframe_insert(data_path="rotation_euler", frame=AnimationConstants.TURNTABLE_FRAME_END)

    # Set the scene to play the animation
    bpy.ops.screen.animation_play()

def add_lights():
    for i, position in enumerate(LightingConstants.LIGHT_POSITIONS):
        bpy.ops.object.light_add(type='POINT', location=position)
        light = bpy.context.active_object
        light.name = f"{FileConstants.TURNTABLE_LIGHT_PREFIX}{i+1}"
        light.data.energy = LightingConstants.LIGHT_ENERGY
