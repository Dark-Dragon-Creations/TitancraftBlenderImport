import bpy  # type: ignore
import os
from .utils import arrange_nodes
from .constants import MaterialConstants, ImportConstants, ViewportConstants

def apply_textures(obj_path, texture_paths, base_name, ior=MaterialConstants.DEFAULT_IOR, configuration=ImportConstants.CONFIGURATION_DEFAULT):
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
    material = bpy.data.materials.new(name=MaterialConstants.MATERIAL_NAME)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get(MaterialConstants.PRINCIPLED_BSDF_NAME)

    # Create texture nodes
    tex_color_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_normals_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_metallic_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_roughness_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    normal_map_node = material.node_tree.nodes.new('ShaderNodeNormalMap')

    # Load textures
    tex_color_node.image = bpy.data.images.load(texture_paths['color'])
    tex_normals_node.image = bpy.data.images.load(texture_paths['normals'])
    tex_metallic_node.image = bpy.data.images.load(texture_paths['metallic'])
    tex_roughness_node.image = bpy.data.images.load(texture_paths['roughness'])

    # Set the color space of the Normal map to Non-Color
    tex_normals_node.image.colorspace_settings.name = MaterialConstants.NON_COLOR_SPACE
    tex_metallic_node.image.colorspace_settings.name = MaterialConstants.NON_COLOR_SPACE
    tex_roughness_node.image.colorspace_settings.name = MaterialConstants.NON_COLOR_SPACE

    # Connect texture nodes to the Principled BSDF shader
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_color_node.outputs['Color'])
    material.node_tree.links.new(normal_map_node.inputs['Color'], tex_normals_node.outputs['Color'])
    material.node_tree.links.new(bsdf.inputs['Normal'], normal_map_node.outputs['Normal'])
    material.node_tree.links.new(bsdf.inputs['Metallic'], tex_metallic_node.outputs['Color'])
    material.node_tree.links.new(bsdf.inputs['Roughness'], tex_roughness_node.outputs['Color'])

    if configuration != ImportConstants.CONFIGURATION_UNREAL:
        tex_ao_node = material.node_tree.nodes.new('ShaderNodeTexImage')
        tex_ao_node.image = bpy.data.images.load(texture_paths['ao'])
        tex_ao_node.image.colorspace_settings.name = MaterialConstants.NON_COLOR_SPACE

        mix_rgb_node = material.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_rgb_node.blend_type = 'MULTIPLY'
        material.node_tree.links.new(mix_rgb_node.inputs['Color1'], tex_color_node.outputs['Color'])
        material.node_tree.links.new(mix_rgb_node.inputs['Color2'], tex_ao_node.outputs['Color'])
        material.node_tree.links.new(bsdf.inputs['Base Color'], mix_rgb_node.outputs['Color'])

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
        if area.type == ViewportConstants.VIEW_3D_AREA_TYPE:
            for space in area.spaces:
                if space.type == ViewportConstants.VIEW_3D_AREA_TYPE:
                    space.shading.type = ViewportConstants.MATERIAL_PREVIEW_SHADING

    return {'FINISHED'}
