markdown

# Titancraft Import

Titancraft Import is a Blender add-on developed by DarkDragonCreations to streamline the process of importing 3D models and applying textures. This add-on automates the process of importing `.obj` files, applying textures, resizing for Unreal Engine, and setting up materials.

## Features

- Import `.obj` files from a zip archive
- Automatically apply diffuse, normal, and metallic AO roughness textures
- Set the Index of Refraction (IOR) for the material
- Resize models for Unreal Engine
- Clean up default Blender objects

## Installation

1. **Download the Add-on**

   Download the latest release of the Titancraft Import add-on from the [releases page](https://github.com/Movian/Titancraft_Import/releases).

2. **Install the Add-on in Blender**

   - Open Blender.
   - Go to `Edit > Preferences > Add-ons > Install...`.
   - Select the downloaded `Titancraft_Import.zip` file.
   - Enable the add-on by checking the box next to `Titancraft Import`.

## Usage

1. **Importing a Model**

   - Go to `File > Import > Titancraft (.zip)`.
   - In the file browser, select the zip file containing your `.obj` file and textures.
   - Adjust the IOR and Resize for UE settings if needed.
   - Click `Import Titancraft (.zip)` to import the model.

2. **Expected Zip File Structure**

   The zip file should contain:
   - `model.obj`: The 3D model file.
   - `model Albedo.png`: The diffuse texture.
   - `model Normals.png`: The normal map texture.
   - `model Metallic AO Roughness.png`: The metallic AO roughness texture.

3. **Properties**

   - **IOR**: Set the Index of Refraction for the material. Default is `1.05`.
   - **Resize for UE**: Toggle whether to resize the model for Unreal Engine. Default is `True`.

## Development

### Folder Structure

Titancraft_Import/
init.py
operator.py
functions/
cleanup.py
apply_textures.py
resize.py
utils.py

markdown


### Scripts

- `__init__.py`: Initialization script for the add-on.
- `operator.py`: Main operator script for handling the import process.
- `functions/cleanup.py`: Script for cleaning up default Blender objects.
- `functions/apply_textures.py`: Script for applying textures to the imported model.
- `functions/resize.py`: Script for resizing the imported model.
- `functions/utils.py`: Utility functions for node arrangement and other tasks.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/Movian/Titancraft_Import).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

