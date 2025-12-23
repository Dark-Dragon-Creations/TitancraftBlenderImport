markdown

# Titancraft Import

Titancraft Import is a Blender add-on developed by DarkDragonCreations to streamline the process of importing 3D models and applying textures. This add-on automates the process of importing `.obj` files, applying textures, resizing for Unreal Engine, and setting up materials.

# AI Dosclosure

This Add one is created and maintained with the assistance of Github Copilot.

tool is utilized for the following

- Debuging Assistance.
- Simple Function Creation.
- Refactoring suggestions.
- Lookup of property values and options.

Tool is NOT used for vibe coding and is only used to enhance coding process. Anyone branching or forking is requested to stick with this limitation.

## Features

- **One-Click Import**: Import `.obj` files and textures from a zip archive
- **Automatic Material Setup**: Apply diffuse, normal, metallic, roughness, and AO textures
- **Multiple Import Modes**: 
  - Default configuration with full material setup
  - Unreal Engine optimized (excludes AO, applies proper scaling)
  - Turntable mode with rotating camera and lighting
- **Smart File Detection**: Handles both flat and subdirectory zip structures
- **Customizable Materials**: Set Index of Refraction (IOR) for realistic materials
- **Scene Management**: Clean up default objects and rename collections
- **Professional Logging**: Clear feedback and error reporting in Blender's UI

## Installation

1 A. **Download the Add-on**

   Download the latest release of the Titancraft Import add-on from the [releases page](https://github.com/Dark-Dragon-Creations/TitancraftBlenderImport/releases).

1 B. **Download the Latest**

   Download the latest Source code, extract the files and then create a zip file from the Titancraft_Import folder excluding the readme and supporting git files, name the file Titancraft_Import.zip this will ensure you have the latest changes (Treat this as a BETA as you will have the most recent coding changes).

2. **Install the Add-on in Blender**

   - Open Blender.
   - Go to `Edit > Preferences > Add-ons > Install...`.
   - Select the downloaded `Titancraft_Import.zip` file.
   - Enable the add-on by checking the box next to `Titancraft Import`.

## Usage

1. **Importing a Model**

   - Go to `File > Import > Titancraft (.zip)`.
   - In the file browser, select the zip file containing your `.obj` file and textures.
   - Configure the import settings:
     - Set the **IOR** (Index of Refraction) for the material
     - Choose the **Import For** mode (Default/Unreal/Turntable)
     - Toggle **Remove Default Objects** and **Rename Objects** as needed
   - Click `Import Titancraft (.zip)` to import the model.

2. **Expected Zip File Structure**

   The zip file should contain:
   - `{model_name}.obj`: The 3D model file.
   - `{model_name}_color.png`: The diffuse/albedo texture.
   - `{model_name}_normals.png`: The normal map texture.
   - `{model_name}_metallic.png`: The metallic texture.
   - `{model_name}_roughness.png`: The roughness texture.
   - `{model_name}_ao.png`: The ambient occlusion texture.
   - `{model_name}_emissive.png`: The ambient occlusion texture.

3. **Properties**

   - **IOR**: Set the Index of Refraction for the material. Default is `1.05`.
   - **Import For**: Select the configuration type:
     - **Default**: Standard import with full material setup including AO
     - **Unreal**: Optimized for Unreal Engine (excludes AO, applies UE scaling)
     - **Turntable**: Adds rotating camera and lighting for presentation
   - **Remove Default Objects**: Remove the default camera, cube, and light. Default is `True`.
   - **Rename Objects**: Rename the Collection and imported object. Default is `True`.

## Development

### Folder Structure

```
Titancraft_Import/
├── __init__.py
├── operator.py
└── functions/
    ├── cleanup.py
    ├── apply_textures.py
    ├── resize.py
    ├── turntable.py
    ├── utils.py
    ├── io.py
    ├── constants.py
    └── logging_utils.py
```

### Scripts

- `__init__.py`: Initialization script for the add-on.
- `operator.py`: Main operator script for handling the import process.
- `functions/cleanup.py`: Script for cleaning up default Blender objects.
- `functions/apply_textures.py`: Script for applying textures to the imported model.
- `functions/resize.py`: Script for resizing the imported model.
- `functions/turntable.py`: Script for setting up turntable camera and lighting.
- `functions/utils.py`: Utility functions for node arrangement and file checking.
- `functions/io.py`: File handling utilities for zip extraction and path management.
- `functions/constants.py`: Centralized constants for all magic numbers and configuration.
- `functions/logging_utils.py`: Professional logging and error reporting system.

## Troubleshooting

### Common Issues

**"No mesh objects found after import"**
- Ensure your zip file contains a valid `.obj` file
- Check that the `.obj` file is not corrupted

**"Missing texture files"**
- Verify all required texture files are present in the zip
- Check that texture files follow the naming convention: `{model_name}_color.png`, `{model_name}_normals.png`, etc.

**"OBJ file not found"**
- Ensure the `.obj` file is named correctly: `{model_name}.obj`
- Check that the zip file structure is correct (files can be in root or a single subdirectory)

### File Naming Convention

The add-on expects files to be named using the following pattern:
- Model: `{model_name}.obj`
- Textures: `{model_name}_{texture_type}.png`

Where `{texture_type}` can be: `color`, `normals`, `metallic`, `roughness`, `ao`

### Logging

The add-on provides detailed logging information:
- **Info messages**: Show in Blender's UI for important operations
- **Error messages**: Display in Blender's UI when something goes wrong
- **Debug messages**: Available in Blender's console for troubleshooting

To view debug messages in Blender:
1. Open the Python Console (`Window > Toggle System Console`)
2. Run the import operation
3. Check the console output for detailed information

## Version History

- **V1.0** (Current): Complete rewrite with constants, professional logging, and multiple import modes
- **V0.95**: Updated utils.py
- **V0.9**: Updated README.md
- **V0.8**: Removed Gif Maker functionality


