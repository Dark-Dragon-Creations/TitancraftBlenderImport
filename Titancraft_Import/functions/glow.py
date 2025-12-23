import bpy  # type: ignore
from .logging_utils import get_logger, log_operation_start, log_operation_success

def setup_glow_compositor(operator=None):
    """Setup compositor with bloom/glow effect."""
    logger = get_logger(operator)
    log_operation_start("glow compositor setup", logger)
    
    # Enable use nodes in the compositor
    bpy.context.scene.use_nodes = True
    logger.info("Enabled compositor nodes")
    
    # Turn on realtime compositing
    bpy.context.scene.render.use_compositing = True
    logger.info("Enabled realtime compositing")
    
    # Enable viewport compositing shading (Always)
    # Set for all workspaces (Layout, Shading, etc.)
    for workspace in bpy.data.workspaces:
        for screen in workspace.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.use_compositor = 'ALWAYS'
                            logger.info(f"Enabled viewport compositing to 'ALWAYS' for workspace: {workspace.name}")
                            break
    
    # Get the compositor node tree
    node_tree = bpy.context.scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links
    
    # Clear existing nodes
    nodes.clear()
    
    # Create Render Layers node
    render_layers_node = nodes.new(type='CompositorNodeRLayers')
    render_layers_node.location = (0, 0)
    logger.debug("Created Render Layers node")
    
    # Create Glare node and set to Fog Glow
    glare_node = nodes.new(type='CompositorNodeGlare')
    glare_node.glare_type = 'BLOOM'
    glare_node.location = (300, 0)
    logger.info("Created Glare node with BLOOM type")
    
    # Create Composite node
    composite_node = nodes.new(type='CompositorNodeComposite')
    composite_node.location = (600, 0)
    logger.debug("Created Composite node")
    
    # Link nodes together
    links.new(render_layers_node.outputs['Image'], glare_node.inputs['Image'])
    links.new(glare_node.outputs['Image'], composite_node.inputs['Image'])
    logger.info("Connected compositor nodes")
    
    log_operation_success("glow compositor setup", logger)
