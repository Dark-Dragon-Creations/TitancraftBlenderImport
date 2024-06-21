import bpy  # type: ignore
import os

from utils import arrange_nodes

def apply_textures(obj_path, texture_paths, output_folder, base_name, ior, x_offset, y_offset):
    print("Applying textures...")
    # Import the .obj file
    bpy.ops.wm.obj_import(filepath=obj_path)
    
    # Get the imported object
    obj = bpy.context.selected_objects[0]

    # Create a new material
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    
    # Create texture nodes
    tex_image_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_normal_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_metallic_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    separate_color_node = material.node_tree.nodes.new('ShaderNodeSeparateColor')  # Use the Separate Color node

    # Load textures
    tex_image_node.image = bpy.data.images.load(texture_paths['diffuse'])
    tex_normal_node.image = bpy.data.images.load(texture_paths['normal'])
    tex_metallic_node.image = bpy.data.images.load(texture_paths['metallic'])

    # Set the color space of the Normal map to Non-Color
    tex_normal_node.image.colorspace_settings.name = 'Non-Color'

    # Connect texture nodes to the Principled BSDF shader
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image_node.outputs['Color'])
    material.node_tree.links.new(bsdf.inputs['Normal'], tex_normal_node.outputs['Color'])
    
    # Connect Metallic AO Roughness to Separate Color node
    material.node_tree.links.new(separate_color_node.inputs['Color'], tex_metallic_node.outputs['Color'])

    # Connect Separate Color node outputs to the BSDF shader
    material.node_tree.links.new(bsdf.inputs['Metallic'], separate_color_node.outputs['Red'])
    material.node_tree.links.new(bsdf.inputs['Roughness'], separate_color_node.outputs['Green'])

    # Set the IOR
    bsdf.inputs['IOR'].default_value = ior

    # Arrange nodes
    arrange_nodes(material.node_tree, x_offset, y_offset)

    # Assign material to the object
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

    # Set viewport shading to Material Preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
