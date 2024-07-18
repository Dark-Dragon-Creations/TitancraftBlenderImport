import json
from PIL import Image
import os

def create_gif(config):
    image_folder = config["image_folder"]
    output_path = config["output_path"]
    total_duration = config["total_duration"]
    
    # Check if the input image folder exists
    if not os.path.exists(image_folder):
        print(f"Image folder '{image_folder}' does not exist.")
        return
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory '{output_dir}'.")

    images = []
    for file_name in sorted(os.listdir(image_folder)):
        if file_name.endswith('.png'):
            file_path = os.path.join(image_folder, file_name)
            images.append(Image.open(file_path))
    
    if not images:
        print(f"No PNG images found in the folder '{image_folder}'.")
        return

    # Calculate the duration for each frame
    frame_duration = total_duration / len(images)
    
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=int(frame_duration),
        loop=0
    )
    print(f"GIF saved to {output_path}")

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    create_gif(config)
