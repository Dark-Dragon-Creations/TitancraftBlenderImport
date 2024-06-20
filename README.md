# TitanCraftBlenderAutomation
 Automates the process of importing and hooking up textures for titancraft obj downloads

This project automates the process of importing an OBJ file into Blender, applying textures, and optionally exporting the result as an OBJ file. The automation is configured via a config.json file, which allows for flexibility and customization.
Features

    Import OBJ files into Blender
    Apply diffuse, normal, and metallic textures
    Optionally export the scene as an OBJ file with an MTL file and supporting textures
    Automatically launch Blender with the generated .blend file if desired
    Scale the imported object for Unreal Engine if needed

Configuration

All configurations are managed through a config.json file. The following options are available:

    export_obj: Boolean flag to export the scene as an OBJ file.
    blender_executable: Path to the Blender executable.
    launch_blender: Boolean flag to automatically launch Blender with the generated .blend file after export.
    scale_for_ue: Boolean flag to scale the object for Unreal Engine.

Example Configuration (config.json)

json

{
    "export_obj": true,
    "blender_executable": "C:\\Program Files\\Blender Foundation\\Blender 4.1\\blender.exe",
    "launch_blender": true,
    "scale_for_ue": true
}

Project Structure

    ProcessModel.py: Main script to handle the extraction of files, read configuration, and invoke Blender.
    blender_script.py: Blender script to import OBJ, apply textures, and handle optional tasks like exporting OBJ or scaling for UE.

Usage

    Ensure Blender is installed and the path to the executable is correctly set in config.json.
    Place your input ZIP file in the Input folder. The ZIP file should contain:
        An OBJ file
        A diffuse texture (*_Albedo.png)
        A normal texture (*_Normals.png)
        A metallic AO roughness texture (*_Metallic_AO_Roughness.png)
    Run the ProcessModel.py script:

    sh

    python ProcessModel.py

    Check the Output folder for the generated files.

Example Input File Naming

    example.zip:
        example.obj
        example_Albedo.png
        example_Normals.png
        example_Metallic_AO_Roughness.png

Installation

    Clone the repository:

    sh

git clone https://github.com/movian/blender-automation.git
cd blender-automation

Install required Python packages:

sh

    pip install -r requirements.txt

    (Note: Add a requirements.txt file if there are any dependencies. Currently, the scripts use standard libraries.)

Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.
License

This project is licensed under the MIT License.
Additional Information
Notes

    Make sure the paths in config.json are correctly set, especially the blender_executable path.
    The blender_script.py script is designed to be invoked by Blender and not directly from the command line.

Troubleshooting

    If Blender does not start, check the blender_executable path in config.json.
    Ensure all texture files are correctly named and placed inside the ZIP file.
    Check the console output for any error messages.