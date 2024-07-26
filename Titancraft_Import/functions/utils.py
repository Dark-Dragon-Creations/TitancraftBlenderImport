import bpy  # type: ignore
import os

def arrange_nodes(node_tree):
    # Define absolute coordinates for each node type
    tex_color_coords = (-600, 400)
    tex_normals_coords = (-600, 200)
    tex_metallic_coords = (-600, 0)
    tex_ao_coords = (-600, -200)
    tex_roughness_coords = (-600, -400)
    normal_map_coords = (-300, 200)
    mix_rgb_coords = (-300, 400)
    bsdf_coords = (0, 0)
    output_coords = (300, 0)

    for node in node_tree.nodes:
        print(f"Processing node: {node.name}, type: {node.type}, current location: {node.location}")
        if node.type == 'TEX_IMAGE':
            if node.image.name.endswith('normals.png'):
                node.location = tex_normals_coords
                print(f"Moved Normals node to {tex_normals_coords}")
            elif node.image.name.endswith('metallic.png'):
                node.location = tex_metallic_coords
                print(f"Moved Metallic node to {tex_metallic_coords}")
            elif node.image.name.endswith('ao.png'):
                node.location = tex_ao_coords
                print(f"Moved AO node to {tex_ao_coords}")
            elif node.image.name.endswith('roughness.png'):
                node.location = tex_roughness_coords
                print(f"Moved Roughness node to {tex_roughness_coords}")
            else:
                node.location = tex_color_coords
                print(f"Moved Color node to {tex_color_coords}")
        elif isinstance(node, bpy.types.ShaderNodeNormalMap):
            node.location = normal_map_coords
            print(f"Moved Normal Map node to {normal_map_coords}")
        elif isinstance(node, bpy.types.ShaderNodeMixRGB):
            node.location = mix_rgb_coords
            print(f"Moved MixRGB node to {mix_rgb_coords}")
        elif node.type == 'BSDF_PRINCIPLED':
            node.location = bsdf_coords
            print(f"Moved Principled BSDF node to {bsdf_coords}")
        elif node.type == 'OUTPUT_MATERIAL':
            node.location = output_coords
            print(f"Moved Material Output node to {output_coords}")
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
