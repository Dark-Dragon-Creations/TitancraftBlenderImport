def arrange_nodes(node_tree, x_offset, y_offset):
    node_height = 400  # Adjust this value to match the actual height of your nodes
    x_location = 0
    y_location = 0
    tex_y_offset = 800 - node_height  # Move all textures down by the height of one node

    # Initialize positions for switching
    normal_node_position = (-x_offset * 2, tex_y_offset - y_offset)
    metallic_node_position = (-x_offset * 2, tex_y_offset - 2 * y_offset)
    separate_color_position = (-x_offset * 1, tex_y_offset - y_offset + 200)  # Move it further up

    for node in node_tree.nodes:
        print(f"Processing node: {node.name}, type: {node.type}")
        if node.type == 'TEX_IMAGE':
            if node.image.name.endswith('Normals.png'):
                node.location = normal_node_position  # Switch with normal node position
                print(f"Moved Normals node to {normal_node_position}")
            elif node.image.name.endswith('Metallic AO Roughness.png'):
                node.location = metallic_node_position  # Switch with metallic node position
                print(f"Moved Metallic AO Roughness node to {metallic_node_position}")
            else:
                node.location = (-x_offset * 2, tex_y_offset)
                print(f"Moved texture node to {(-x_offset * 2, tex_y_offset)}")
            tex_y_offset -= y_offset
        elif node.type == 'ShaderNodeSeparateColor':  # Ensure we're using the Separate Color node
            node.location = separate_color_position
            print(f"Moved Separate Color node to {separate_color_position}")
        else:
            node.location = (x_location, y_location)
            x_location += x_offset
            print(f"Moved other node to {(x_location, y_location)}")
        y_location -= y_offset
