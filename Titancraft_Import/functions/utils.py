import bpy  # type: ignore
import os
from .constants import NodeConstants, FileConstants

def arrange_nodes(node_tree):
    # Use constants for node positioning
    positions = NodeConstants.NODE_POSITIONS

    for node in node_tree.nodes:
        print(f"Processing node: {node.name}, type: {node.type}, current location: {node.location}")
        if node.type == 'TEX_IMAGE':
            if node.image.name.endswith('normals.png'):
                node.location = positions['tex_normals']
                print(f"Moved Normals node to {positions['tex_normals']}")
            elif node.image.name.endswith('metallic.png'):
                node.location = positions['tex_metallic']
                print(f"Moved Metallic node to {positions['tex_metallic']}")
            elif node.image.name.endswith('ao.png'):
                node.location = positions['tex_ao']
                print(f"Moved AO node to {positions['tex_ao']}")
            elif node.image.name.endswith('roughness.png'):
                node.location = positions['tex_roughness']
                print(f"Moved Roughness node to {positions['tex_roughness']}")
            else:
                node.location = positions['tex_color']
                print(f"Moved Color node to {positions['tex_color']}")
        elif isinstance(node, bpy.types.ShaderNodeNormalMap):
            node.location = positions['normal_map']
            print(f"Moved Normal Map node to {positions['normal_map']}")
        elif isinstance(node, bpy.types.ShaderNodeMixRGB):
            node.location = positions['mix_rgb']
            print(f"Moved MixRGB node to {positions['mix_rgb']}")
        elif node.type == 'BSDF_PRINCIPLED':
            node.location = positions['bsdf']
            print(f"Moved Principled BSDF node to {positions['bsdf']}")
        elif node.type == 'OUTPUT_MATERIAL':
            node.location = positions['output']
            print(f"Moved Material Output node to {positions['output']}")
        else:
            print(f"Node {node.name} of type {node.type} not moved.")
        print(f"Node {node.name} new location: {node.location}")

def check_files_exist(obj_path, texture_paths):
    extracted_files = os.listdir(os.path.dirname(obj_path))
    print(f"Extracted files: {extracted_files}")

    print(f"OBJ file path: {obj_path}")
    print(f"AO texture path: {texture_paths['ao']}")
    print(f"Color texture path: {texture_paths['color']}")
    print(f"Metallic texture path: {texture_paths['metallic']}")
    print(f"Normals texture path: {texture_paths['normals']}")
    print(f"Roughness texture path: {texture_paths['roughness']}")

    if not os.path.exists(obj_path):
        print(f"OBJ file not found: {obj_path}")
        return False
    for key, path in texture_paths.items():
        if not os.path.exists(path):
            print(f"Texture file not found: {path}")
            return False
    return True

def get_subdirectory_path(extract_to):
    subdirectories = [os.path.join(extract_to, d) for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]
    if len(subdirectories) == 1:
        subdirectory_path = subdirectories[0]
        print(f"Subdirectory path: {subdirectory_path}")
        return subdirectory_path
    return None
