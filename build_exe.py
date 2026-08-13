"""
Slime Shooterz - Complete Build Script with Multi-Size Icon
Developed by MANBOY
"""

import os
import sys
import shutil
import subprocess
import glob

def clean_build():
    """Clean previous build files"""
    folders_to_remove = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Removed {folder}/")
    
    for file in glob.glob("*.spec"):
        os.remove(file)
        print(f"Removed {file}")

def check_icon():
    """Check if icon exists and is valid"""
    icon_path = "icon.ico"
    
    if not os.path.exists(icon_path):
        print("⚠️  icon.ico not found! Creating one...")
        try:
            # Try to create icon
            from PIL import Image, ImageDraw
            
            # Create multi-size icon
            sizes = [16, 24, 32, 48, 64, 128, 256]
            icon_images = []
            
            for size in sizes:
                image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(image)
                
                padding = size * 0.15
                # Main body
                draw.ellipse([padding, padding, size - padding, size - padding * 0.7], 
                           fill=(50, 205, 50, 255))
                # Inner glow
                inner_padding = padding * 1.5
                draw.ellipse([inner_padding, inner_padding, size - inner_padding, size - inner_padding * 0.7], 
                           fill=(136, 255, 0, 180))
                # Eyes
                eye_size = size * 0.12
                eye_y = size * 0.35
                draw.ellipse([size * 0.25, eye_y, size * 0.25 + eye_size * 2, eye_y + eye_size * 2], 
                           fill=(255, 255, 255, 255))
                draw.ellipse([size * 0.25 + eye_size * 0.5, eye_y + eye_size * 0.5, 
                              size * 0.25 + eye_size * 1.5, eye_y + eye_size * 1.5], 
                           fill=(0, 0, 0, 255))
                draw.ellipse([size * 0.6, eye_y, size * 0.6 + eye_size * 2, eye_y + eye_size * 2], 
                           fill=(255, 255, 255, 255))
                draw.ellipse([size * 0.6 + eye_size * 0.5, eye_y + eye_size * 0.5, 
                              size * 0.6 + eye_size * 1.5, eye_y + eye_size * 1.5], 
                           fill=(0, 0, 0, 255))
                # Mouth
                mouth_y = size * 0.55
                mouth_width = size * 0.35
                draw.arc([size//2 - mouth_width, mouth_y, size//2 + mouth_width, mouth_y + size * 0.2], 
                         0, 180, fill=(0, 0, 0, 255), width=max(2, size // 20))
                icon_images.append(image)
            
            # Save all sizes
            if icon_images:
                icon_images[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes], 
                                   append_images=icon_images[1:])
                print("✅ Created icon.ico with multiple sizes")
                return True
                
        except ImportError:
            print("❌ PIL not installed. Install with: pip install pillow")
            print("   Continuing without icon...")
            return False
        except Exception as e:
            print(f"❌ Failed to create icon: {e}")
            return False
    
    # Check if icon has multiple sizes
    try:
        import PIL.Image
        icon = PIL.Image.open(icon_path)
        print(f"✅ Icon found: {icon_path}")
        print(f"   Sizes: {icon.info.get('sizes', ['unknown'])}")
        return True
    except:
        print(f"✅ Icon found: {icon_path}")
        return True

def build_exe():
    """Build the executable with icon and all assets"""
    print("=" * 60)
    print("  SLIME SHOOTERZ - BUILD SCRIPT")
    print("  Developed by MANBOY")
    print("=" * 60)
    print()
    
    # Check icon
    print("[0/4] Checking icon...")
    has_icon = check_icon()
    print()
    
    # Clean previous builds
    print("[1/4] Cleaning previous builds...")
    clean_build()
    
    # Install PyInstaller if not installed
    print("[2/4] Checking PyInstaller...")
    try:
        import PyInstaller
        print("  PyInstaller already installed")
    except ImportError:
        print("  Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable with ALL assets and icon
    print("[3/4] Building SlimeShooterz.exe with all assets...")
    print("  This may take 2-3 minutes...")
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "SlimeShooterz",
        "--add-data", "assets;assets",
        "--add-data", "logo.png;.",
        "--add-data", "assets/logo.png;assets",
        "--hidden-import", "pygame",
        "--hidden-import", "pygame.mixer",
        "--hidden-import", "pygame.image",
        "--collect-all", "pygame",
    ]
    
    # Add icon if it exists
    if has_icon and os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
        print("  ✅ Using icon: icon.ico")
    else:
        print("  ❌ No icon found - skipping")
    
    cmd.append("main.py")
    
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        print(f"Build failed: {e}")
        print("\nTrying alternative build command...")
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--add-data", "assets;assets",
            "--add-data", "logo.png;.",
            "main.py",
            "--name", "SlimeShooterz"
        ]
        if has_icon and os.path.exists("icon.ico"):
            cmd.extend(["--icon", "icon.ico"])
        subprocess.check_call(cmd)
    
    print()
    print("[4/4] Build complete!")
    print("=" * 60)
    print()
    print("Your executable is ready at:")
    exe_path = os.path.abspath("dist/SlimeShooterz.exe")
    print(f"  {exe_path}")
    print()
    print("FILE INFO:")
    if os.path.exists("dist/SlimeShooterz.exe"):
        size = os.path.getsize("dist/SlimeShooterz.exe")
        size_mb = size / (1024 * 1024)
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Icon: {'✅ Included' if has_icon else '❌ Not included'}")
    print()
    print("To share with your friend:")
    print("  1. Copy SlimeShooterz.exe from the 'dist' folder")
    print("  2. Send ONLY the EXE file (it contains everything!)")
    print("  3. They just double-click to play!")
    print()
    print("✅ All assets (images, sounds, logo, icon) are embedded inside the EXE!")
    print("=" * 60)

if __name__ == "__main__":
    build_exe()