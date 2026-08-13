"""
Create a complete icon with multiple sizes for Slime Shooterz
Developed by MANBOY
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_complete_icon():
    """Create an icon with multiple sizes for all Windows contexts"""
    
    # Define all sizes needed for Windows
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Create a list to hold all icon images
    icon_images = []
    
    for size in sizes:
        # Create a new image for each size
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Scale everything based on size
        padding = size * 0.15
        center = size // 2
        
        # Main body (green slime blob)
        draw.ellipse([padding, padding, size - padding, size - padding * 0.7], 
                     fill=(50, 205, 50, 255))
        
        # Inner glow
        inner_padding = padding * 1.5
        draw.ellipse([inner_padding, inner_padding, size - inner_padding, size - inner_padding * 0.7], 
                     fill=(136, 255, 0, 180))
        
        # Eyes - scale based on size
        eye_size = size * 0.12
        eye_y = size * 0.35
        
        # Left eye
        draw.ellipse([size * 0.25, eye_y, size * 0.25 + eye_size * 2, eye_y + eye_size * 2], 
                     fill=(255, 255, 255, 255))
        draw.ellipse([size * 0.25 + eye_size * 0.5, eye_y + eye_size * 0.5, 
                      size * 0.25 + eye_size * 1.5, eye_y + eye_size * 1.5], 
                     fill=(0, 0, 0, 255))
        
        # Right eye
        draw.ellipse([size * 0.6, eye_y, size * 0.6 + eye_size * 2, eye_y + eye_size * 2], 
                     fill=(255, 255, 255, 255))
        draw.ellipse([size * 0.6 + eye_size * 0.5, eye_y + eye_size * 0.5, 
                      size * 0.6 + eye_size * 1.5, eye_y + eye_size * 1.5], 
                     fill=(0, 0, 0, 255))
        
        # Mouth (evil grin)
        mouth_y = size * 0.55
        mouth_width = size * 0.35
        draw.arc([center - mouth_width, mouth_y, center + mouth_width, mouth_y + size * 0.2], 
                 0, 180, fill=(0, 0, 0, 255), width=max(2, size // 20))
        
        # For smaller sizes, add a simple smile
        if size < 32:
            draw.arc([center - mouth_width * 0.5, mouth_y, center + mouth_width * 0.5, mouth_y + size * 0.15], 
                     0, 180, fill=(0, 0, 0, 255), width=1)
        
        # Save the image for this size
        icon_images.append(image)
    
    # Save all sizes into one ICO file
    if icon_images:
        # Save the first image (largest) as the base
        icon_images[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes], 
                           append_images=icon_images[1:])
        print(f"✅ Created complete icon.ico with sizes: {sizes}")
        print(f"   Location: {os.path.abspath('icon.ico')}")
        return True
    else:
        print("❌ Failed to create icon")
        return False

if __name__ == "__main__":
    # Check if PIL is installed
    try:
        from PIL import Image, ImageDraw
        create_complete_icon()
    except ImportError:
        print("PIL not installed. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("PIL installed. Running icon creation...")
        create_complete_icon()