import bpy  # type: ignore

def setup_turntable_camera():
    # Add a camera
    bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(1.1, 0, 0))  # Placing the camera further away and higher
    camera = bpy.context.active_object
    camera.name = "Turntable_Camera"

    # Add an empty object at the center of the model
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))  # Adjust the Z location to be the center
    empty = bpy.context.active_object
    empty.name = "Turntable_Empty"

    # Set the camera to look at the empty object
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = empty
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Parent the camera to the empty object
    camera.parent = empty

    # Set up the animation for the empty object
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 150  # 5 seconds at 30 FPS

    empty.rotation_euler = (0, 0, 0)
    empty.keyframe_insert(data_path="rotation_euler", frame=1)
    empty.rotation_euler = (0, 0, 6.28319)  # 360 degrees in radians
    empty.keyframe_insert(data_path="rotation_euler", frame=150)

    # Set the scene to play the animation
    bpy.ops.screen.animation_play()

def add_lights():
    light_distance = 5
    light_height = 2

    # Positions for the lights (N, E, S, W)
    light_positions = [
        (0, -light_distance, light_height),
        (light_distance, 0, light_height),
        (0, light_distance, light_height),
        (-light_distance, 0, light_height)
    ]

    for i, position in enumerate(light_positions):
        bpy.ops.object.light_add(type='POINT', location=position)
        light = bpy.context.active_object
        light.name = f"Turntable_Light_{i+1}"
        light.data.energy = 1000  # Adjust the intensity as needed
