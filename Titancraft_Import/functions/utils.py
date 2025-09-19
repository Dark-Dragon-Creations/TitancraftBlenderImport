import bpy  # type: ignore
import os
from .constants import NodeConstants, FileConstants
from .logging_utils import get_logger, log_node_operation, log_file_operation

def arrange_nodes(node_tree, logger=None):
    """Arrange shader nodes in the material editor for better organization."""
    if logger is None:
        logger = get_logger()
    
    # Use constants for node positioning
    positions = NodeConstants.NODE_POSITIONS

    for node in node_tree.nodes:
        log_node_operation(node.name, f"processing {node.type} at {node.location}", logger)
        
        if node.type == 'TEX_IMAGE':
            if node.image.name.endswith('normals.png'):
                node.location = positions['tex_normals']
                log_node_operation(node.name, f"moved to {positions['tex_normals']}", logger)
            elif node.image.name.endswith('metallic.png'):
                node.location = positions['tex_metallic']
                log_node_operation(node.name, f"moved to {positions['tex_metallic']}", logger)
            elif node.image.name.endswith('ao.png'):
                node.location = positions['tex_ao']
                log_node_operation(node.name, f"moved to {positions['tex_ao']}", logger)
            elif node.image.name.endswith('roughness.png'):
                node.location = positions['tex_roughness']
                log_node_operation(node.name, f"moved to {positions['tex_roughness']}", logger)
            else:
                node.location = positions['tex_color']
                log_node_operation(node.name, f"moved to {positions['tex_color']}", logger)
        elif isinstance(node, bpy.types.ShaderNodeNormalMap):
            node.location = positions['normal_map']
            log_node_operation(node.name, f"moved to {positions['normal_map']}", logger)
        elif isinstance(node, bpy.types.ShaderNodeMixRGB):
            node.location = positions['mix_rgb']
            log_node_operation(node.name, f"moved to {positions['mix_rgb']}", logger)
        elif node.type == 'BSDF_PRINCIPLED':
            node.location = positions['bsdf']
            log_node_operation(node.name, f"moved to {positions['bsdf']}", logger)
        elif node.type == 'OUTPUT_MATERIAL':
            node.location = positions['output']
            log_node_operation(node.name, f"moved to {positions['output']}", logger)
        else:
            log_node_operation(node.name, f"not moved (unsupported type: {node.type})", logger)

def check_files_exist(obj_path, texture_paths, logger=None):
    """Check if all required files exist and log the results."""
    if logger is None:
        logger = get_logger()
    
    extracted_files = os.listdir(os.path.dirname(obj_path))
    logger.debug(f"Extracted files: {extracted_files}")

    # Log file paths for debugging
    log_file_operation("Checking OBJ file", obj_path, logger)
    for key, path in texture_paths.items():
        log_file_operation(f"Checking {key} texture", path, logger)

    if not os.path.exists(obj_path):
        logger.error(f"OBJ file not found: {obj_path}")
        return False
    
    missing_textures = []
    for key, path in texture_paths.items():
        if not os.path.exists(path):
            missing_textures.append(f"{key}: {path}")
    
    if missing_textures:
        logger.error(f"Missing texture files: {', '.join(missing_textures)}")
        return False
    
    logger.info("All required files found")
    return True

def get_subdirectory_path(extract_to, logger=None):
    """Find subdirectory if files are not in root of extracted folder."""
    if logger is None:
        logger = get_logger()
    
    subdirectories = [os.path.join(extract_to, d) for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]
    if len(subdirectories) == 1:
        subdirectory_path = subdirectories[0]
        logger.debug(f"Found subdirectory: {subdirectory_path}")
        return subdirectory_path
    return None
