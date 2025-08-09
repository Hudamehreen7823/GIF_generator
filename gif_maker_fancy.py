import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(image, text, position=(10, 10), font_size=50):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("Pluretta Vintage DEMO VERSION", font_size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, text, fill="white", font=font, stroke_width=1, stroke_fill="black")
    return image

def create_fade_transition(img1, img2, steps=5):
    fades = []
    for i in range(1, steps + 1):
        alpha = i / (steps + 1)
        blended = Image.blend(img1, img2, alpha)
        fades.append(blended)
    return fades

def create_gif_with_effects(folder, output_path, duration=500, resize=None, text=None, fade_steps=5):
    valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(valid_exts)])
    paths = [os.path.join(folder, f) for f in files]
    
    if not paths:
        raise ValueError("No valid image files found.")

    frames = []

    prev_img = None
    for path in paths:
        img = Image.open(path).convert("RGBA")
        if resize:
            img = img.resize(resize)
        if text:
            img = add_text_overlay(img, text)
        if prev_img:
            frames.extend(create_fade_transition(prev_img, img, fade_steps))
        frames.append(img)
        prev_img = img

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2  # prevent ghosting
    )

    print(f"✅ GIF created with {len(frames)} frames (including fades) at '{output_path}'")

def parse_resize(s):
    try:
        w, h = map(int, s.lower().split('x'))
        return (w, h)
    except:
        raise argparse.ArgumentTypeError("Resize must be in WIDTHxHEIGHT format")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an advanced GIF with text and fade transitions.")
    parser.add_argument("folder", help="Folder with image files")
    parser.add_argument("output", help="Output GIF file path")
    parser.add_argument("--duration", type=int, default=400, help="Frame duration in ms")
    parser.add_argument("--resize", type=parse_resize, help="Resize to WIDTHxHEIGHT (e.g., 400x400)")
    parser.add_argument("--text", type=str, help="Text to overlay on each frame")
    parser.add_argument("--text", type=str, help="Text to overlay on each frame")
    parser.add_argument("--text", type=str, help="Text to overlay on each frame")
    parser.add_argument("--fade-steps", type=int, default=5, help="Number of fade transition frames")

    args = parser.parse_args()

    create_gif_with_effects(
        folder=args.folder,
        output_path=args.output,
        duration=args.duration,
        resize=args.resize,
        text=args.text,
        fade_steps=args.fade_steps
    )
