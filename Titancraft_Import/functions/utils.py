import bpy  # type: ignore

def arrange_nodes(node_tree):
    # Define absolute coordinates for each node type
    tex_image_coords = (-600, 400)
    tex_normal_coords = (-600, -400)
    tex_metallic_coords = (-600, 0)
    separate_color_coords = (-300, -50)
    bsdf_coords = (0, 0)
    output_coords = (300, 0)

    for node in node_tree.nodes:
        print(f"Processing node: {node.name}, type: {node.type}, current location: {node.location}")
        if node.type == 'TEX_IMAGE':
            if node.image.name.endswith('Normals.png'):
                node.location = tex_normal_coords
                print(f"Moved Normals node to {tex_normal_coords}")
            elif node.image.name.endswith('Metallic AO Roughness.png'):
                node.location = tex_metallic_coords
                print(f"Moved Metallic AO Roughness node to {tex_metallic_coords}")
            else:
                node.location = tex_image_coords
                print(f"Moved texture node to {tex_image_coords}")
        elif isinstance(node, bpy.types.ShaderNodeSeparateColor):
            node.location = separate_color_coords
            print(f"Moved Separate Color node to {separate_color_coords}")
        elif node.type == 'BSDF_PRINCIPLED':
            node.location = bsdf_coords
            print(f"Moved Principled BSDF node to {bsdf_coords}")
        elif node.type == 'OUTPUT_MATERIAL':
            node.location = output_coords
            print(f"Moved Material Output node to {output_coords}")
        else:
            print(f"Node {node.name} of type {node.type} not moved.")
        print(f"Node {node.name} new location: {node.location}")
