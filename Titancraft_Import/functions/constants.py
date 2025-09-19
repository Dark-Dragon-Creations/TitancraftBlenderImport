"""
Constants for Titancraft Import add-on.
Contains all magic numbers and configuration values used throughout the add-on.
"""

# Material and Shader Constants
class MaterialConstants:
    """Constants related to materials and shaders."""
    DEFAULT_IOR = 1.05
    MATERIAL_NAME = "Material"
    PRINCIPLED_BSDF_NAME = "Principled BSDF"
    
    # Color space settings
    NON_COLOR_SPACE = 'Non-Color'
    SRGB_COLOR_SPACE = 'sRGB'

# Scaling Constants
class ScalingConstants:
    """Constants related to object scaling and sizing."""
    # Unreal Engine scaling factor (0.054 = 1/18.5, common UE4/UE5 scale)
    UNREAL_ENGINE_SCALE = (0.054, 0.054, 0.054)
    
    # Default scale (no scaling)
    DEFAULT_SCALE = (1.0, 1.0, 1.0)

# Animation Constants
class AnimationConstants:
    """Constants related to turntable animation."""
    TURNTABLE_FRAME_START = 1
    TURNTABLE_FRAME_END = 150  # 5 seconds at 30 FPS
    TURNTABLE_FPS = 30
    TURNTABLE_DURATION_SECONDS = 5.0
    
    # Rotation values (in radians)
    TURNTABLE_ROTATION_START = (0, 0, 0)
    TURNTABLE_ROTATION_END = (0, 0, 6.28319)  # 360 degrees in radians

# Lighting Constants
class LightingConstants:
    """Constants related to lighting setup."""
    LIGHT_ENERGY = 1000
    LIGHT_DISTANCE = 5
    LIGHT_HEIGHT = 2
    
    # Light positions for turntable (N, E, S, W)
    LIGHT_POSITIONS = [
        (0, -LIGHT_DISTANCE, LIGHT_HEIGHT),
        (LIGHT_DISTANCE, 0, LIGHT_HEIGHT),
        (0, LIGHT_DISTANCE, LIGHT_HEIGHT),
        (-LIGHT_DISTANCE, 0, LIGHT_HEIGHT)
    ]

# Camera Constants
class CameraConstants:
    """Constants related to camera setup."""
    TURNTABLE_CAMERA_LOCATION = (0, -5, 2)
    TURNTABLE_CAMERA_ROTATION = (1.1, 0, 0)
    TURNTABLE_EMPTY_LOCATION = (0, 0, 1)
    
    # Camera constraint settings
    TRACK_AXIS = 'TRACK_NEGATIVE_Z'
    UP_AXIS = 'UP_Y'

# Node Positioning Constants
class NodeConstants:
    """Constants for shader node positioning in the material editor."""
    # Node coordinates (x, y) for organized layout
    NODE_POSITIONS = {
        'tex_color': (-600, 600),
        'tex_normals': (-600, 200),
        'tex_metallic': (-600, -100),
        'tex_ao': (-900, 275),
        'tex_roughness': (-600, 900),
        'normal_map': (-300, 200),
        'mix_rgb': (-300, 400),
        'bsdf': (0, 0),
        'output': (300, 0)
    }

# File and Path Constants
class FileConstants:
    """Constants related to file handling and naming."""
    # Default collection and object names
    DEFAULT_COLLECTION_NAME = 'Collection'
    CHARACTER_COLLECTION_NAME = 'Character'
    
    # Object names for cleanup
    DEFAULT_OBJECTS = ['Cube', 'Light', 'Camera']
    
    # Turntable object names
    TURNTABLE_CAMERA_NAME = "Turntable_Camera"
    TURNTABLE_EMPTY_NAME = "Turntable_Empty"
    TURNTABLE_LIGHT_PREFIX = "Turntable_Light_"

# Viewport Constants
class ViewportConstants:
    """Constants related to viewport settings."""
    MATERIAL_PREVIEW_SHADING = 'MATERIAL'
    VIEW_3D_AREA_TYPE = 'VIEW_3D'

# Import Configuration Constants
class ImportConstants:
    """Constants related to import configurations."""
    CONFIGURATION_DEFAULT = 'DEFAULT'
    CONFIGURATION_UNREAL = 'UNREAL'
    CONFIGURATION_TURNTABLE = 'TURNTABLE'
    
    # Supported texture types
    TEXTURE_TYPES = ['color', 'normals', 'metallic', 'roughness', 'ao']
    
    # File extensions
    OBJ_EXTENSION = '.obj'
    ZIP_EXTENSION = '.zip'
    PNG_EXTENSION = '.png'
