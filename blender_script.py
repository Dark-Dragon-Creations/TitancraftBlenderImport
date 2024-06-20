import bpy
import sys
import os
import shutil

def cleanup_default_objects():
    bpy.ops.object.select_all(action='DESELECT')
    
    if 'Cube' in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()
    
    if 'Camera' in bpy.data.objects:
        bpy.data.objects['Camera'].select_set(True)
        bpy.ops.object.delete()
    
    if 'Light' in bpy.data.objects:
        bpy.data.objects['Light'].select_set(True)
        bpy.ops.object.delete()

def set_viewport_shading(mode='MATERIAL'):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = mode

def apply_textures(obj_path, texture_paths, output_folder, base_name, export_obj, scale_for_ue):
    # Cleanup default objects
    cleanup_default_objects()

    # Import the .obj file
    bpy.ops.wm.obj_import(filepath=obj_path)
    
    # Get the imported object
    obj = bpy.context.selected_objects[0]

    if scale_for_ue:
        # Scale the object for Unreal Engine
        obj.scale = (0.054, 0.054, 0.054)
    
    # Create a new material
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    
    # Create texture nodes
    tex_image_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_normal_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_metallic_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    separate_rgb_node = material.node_tree.nodes.new('ShaderNodeSeparateRGB')

    # Load textures
    tex_image_node.image = bpy.data.images.load(texture_paths['diffuse'])
    tex_normal_node.image = bpy.data.images.load(texture_paths['normal'])
    tex_metallic_node.image = bpy.data.images.load(texture_paths['metallic'])

    # Set the color space of the Normal map to Non-Color
    tex_normal_node.image.colorspace_settings.name = 'Non-Color'

    # Connect texture nodes to the Principled BSDF shader
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image_node.outputs['Color'])
    material.node_tree.links.new(bsdf.inputs['Normal'], tex_normal_node.outputs['Color'])
    
    # Connect Metallic AO Roughness to Separate RGB node
    material.node_tree.links.new(separate_rgb_node.inputs['Image'], tex_metallic_node.outputs['Color'])

    # Connect Separate RGB node outputs to the BSDF shader
    material.node_tree.links.new(bsdf.inputs['Metallic'], separate_rgb_node.outputs['R'])
    material.node_tree.links.new(bsdf.inputs['Roughness'], separate_rgb_node.outputs['G'])

    # Set the IOR
    bsdf.inputs['IOR'].default_value = 1.05

    # Assign material to the object
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    
    # Set viewport shading to Material Preview
    set_viewport_shading('MATERIAL')
    
    # Save the Blender file
    output_file_path = os.path.join(output_folder, f"{base_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_file_path)

    if export_obj:
        # Export the scene to OBJ format
        obj_output_path = os.path.join(output_folder, f"{base_name}.obj")
        bpy.ops.wm.obj_export(filepath=obj_output_path)

        # Copy texture files to the output folder
        for key, texture_path in texture_paths.items():
            shutil.copy(texture_path, output_folder)

def main():
    # Parse command line arguments
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    
    obj_path = os.path.abspath(argv[0])
    texture_paths = {
        'diffuse': os.path.abspath(argv[1]),
        'normal': os.path.abspath(argv[2]),
        'metallic': os.path.abspath(argv[3])
    }
    output_folder = os.path.abspath(argv[4])
    base_name = argv[5]
    export_obj = argv[6].lower() == 'true'
    launch_blender = argv[7].lower() == 'true'
    scale_for_ue = argv[8].lower() == 'true'

    # Apply textures
    apply_textures(obj_path, texture_paths, output_folder, base_name, export_obj, scale_for_ue)

if __name__ == "__main__":
    main()
