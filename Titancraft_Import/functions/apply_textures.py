import bpy  # type: ignore
import os
from .utils import arrange_nodes

def apply_textures(obj_path, texture_paths, base_name, ior=1.05, configure_for_unreal=False):
    print("Applying textures...")

    # Import the .obj file
    try:
        bpy.ops.wm.obj_import(filepath=obj_path)
        print(f"Imported OBJ file: {obj_path}")
    except Exception as e:
        print(f"Failed to import .obj file: {e}")
        return {'CANCELLED'}

    # Ensure the imported object is selected and active
    imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if not imported_objects:
        print("No objects imported.")
        return {'CANCELLED'}

    obj = imported_objects[-1]  # Get the last imported object
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    print(f"Selected imported object: {obj.name}")

    # Create a new material
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")

    # Create texture nodes
    tex_image_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_normal_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_metallic_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    separate_color_node = material.node_tree.nodes.new('ShaderNodeSeparateColor')  # Use the Separate Color node
    normal_map_node = material.node_tree.nodes.new('ShaderNodeNormalMap')  # Add Normal Map node

    # Load textures
    tex_image_node.image = bpy.data.images.load(texture_paths['diffuse'])
    tex_normal_node.image = bpy.data.images.load(texture_paths['normal'])
    tex_metallic_node.image = bpy.data.images.load(texture_paths['metallic'])

    # Set the color space of the Normal map to Non-Color
    tex_normal_node.image.colorspace_settings.name = 'Non-Color'

    # Connect texture nodes to the Principled BSDF shader
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image_node.outputs['Color'])  # Albedo to Base Color
    material.node_tree.links.new(normal_map_node.inputs['Color'], tex_normal_node.outputs['Color'])  # Connect Normals Texture to Normal Map node
    material.node_tree.links.new(bsdf.inputs['Normal'], normal_map_node.outputs['Normal'])  # Connect Normal Map node to BSDF

    # Connect Metallic AO Roughness to Separate Color node
    material.node_tree.links.new(separate_color_node.inputs['Color'], tex_metallic_node.outputs['Color'])

    # Connect Separate Color node outputs to the BSDF shader
    material.node_tree.links.new(bsdf.inputs['Metallic'], separate_color_node.outputs['Red'])
    material.node_tree.links.new(bsdf.inputs['Roughness'], tex_metallic_node.outputs['Alpha'])  # Roughness Alpha to BSDF Roughness

    if not configure_for_unreal:
        mix_rgb_node = material.node_tree.nodes.new('ShaderNodeMixRGB')  # Add MixRGB node
        # Set the MixRGB node to Multiply
        mix_rgb_node.blend_type = 'MULTIPLY'
        # Connect the MixRGB node
        material.node_tree.links.new(mix_rgb_node.inputs['Color1'], tex_image_node.outputs['Color'])  # Albedo to Mix A
        material.node_tree.links.new(mix_rgb_node.inputs['Color2'], separate_color_node.outputs['Green'])  # Separate Color Green to Mix B
        material.node_tree.links.new(bsdf.inputs['Base Color'], mix_rgb_node.outputs['Color'])  # MixRGB to Base Color

    # Set the IOR
    bsdf.inputs['IOR'].default_value = ior

    # Arrange nodes
    arrange_nodes(material.node_tree)

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

    return {'FINISHED'}
