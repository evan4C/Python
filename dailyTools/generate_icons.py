from PIL import Image
import os

# Define iOS app icon sizes (in pixels)
IOS_ICON_SIZES = [
    (180, "Icon-60@3x.png"),  # iPhone App (iOS 7-17, 60pt @3x)
    (120, "Icon-60@2x.png"),  # iPhone App (iOS 7-17, 60pt @2x)
    (167, "Icon-83.5@2x.png"),  # iPad Pro App (iOS 9-17, 83.5pt @2x)
    (152, "Icon-76@2x.png"),  # iPad App (iOS 7-17, 76pt @2x)
    (120, "Icon-40@3x.png"),  # Spotlight (iOS 7-17, 40pt @3x)
    (80, "Icon-40@2x.png"),   # Spotlight (iOS 7-17, 40pt @2x)
    (60, "Icon-20@3x.png"),   # Settings/Action (iOS 7-17, 20pt @3x)
    (40, "Icon-20@2x.png"),   # Settings/Action (iOS 7-17, 20pt @2x)
    (20, "Icon-20@1x.png"),   # Settings/Action (iOS 7-17, 20pt @1x)
    (87, "Icon-29@3x.png"),   # Settings/Spotlight (iOS 7-17, 29pt @3x)
    (58, "Icon-29@2x.png"),   # Settings/Spotlight (iOS 7-17, 29pt @2x)
    (29, "Icon-29@1x.png"),   # Settings/Spotlight (iOS 7-17, 29pt @1x)
    (1024, "Icon-1024.png")   # App Store (iOS)
]

def resize_icon(input_path, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the input image
    try:
        img = Image.open(input_path)
        if img.size != (1024, 1024):
            raise ValueError("Input image must be 1024x1024 pixels")
        
        # Process each size
        for size, filename in IOS_ICON_SIZES:
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            output_path = os.path.join(output_dir, filename)
            resized_img.save(output_path, "PNG")
            print(f"Saved {filename} at {size}x{size}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify your input image and output directory
    input_image = "Icon-1024x1024.png"  # Replace with your 1024x1024 PNG file path
    output_directory = "iOS_Icons"  # Output folder for icons
    resize_icon(input_image, output_directory)
