import os
import argparse
import random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
QUOTES = [
    "Believe in yourself!",
    "Shine bright sparkle ",
    "Keep going strong ",
    "Dream big ",
    "Stay curious ",
    "Create magic",
    "Make it happen!",
    "Never give up!",
    "Push your limits "
]
def add_sparkle_text(image, text, position=(10, 10), font_size=28):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("Pluretta Vintage DEMO VERSION", font_size)
    except IOError:
        font = ImageFont.load_default()

    x, y = position
    colors = ["#FF69B4", "#FFD700", "#ADFF2F", "#00FFFF", "#00FFB7"]
    for dx, dy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
        draw.text((x + dx, y + dy), text, font=font, fill=random.choice(colors))
    draw.text((x, y), text, font=font, fill=random.choice(colors))
    return image

def create_fade_transition(img1, img2, steps=5):
    return [Image.blend(img1, img2, i / (steps + 1)).convert("RGBA") for i in range(1, steps + 1)]

def create_gif_with_quotes(folder, output_path, duration=500, resize=None, fade_steps=5):
    valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(valid_exts)])
    paths = [os.path.join(folder, f) for f in files]
    if not paths:
        raise ValueError("No valid image files found in the folder.")
    frames = []
    prev_img = None
    for path in paths:
        img = Image.open(path).convert("RGBA")
        if resize:
            img = img.resize(resize)

        quote = random.choice(QUOTES)
        img = add_sparkle_text(img, quote, position=(70,670), font_size=90)
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
        disposal=2
    )
    print(f"Sparkle GIF created with {len(frames)} frames at '{output_path}'")

def parse_resize(s):
    try:
        w, h = map(int, s.lower().split('x'))
        return (w, h)
    except:
        raise argparse.ArgumentTypeError("Resize must be WIDTHxHEIGHT format")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a sparkling GIF with random quotes.")
    parser.add_argument("folder", help="Folder containing image files")
    parser.add_argument("output", help="Output GIF file path")
    parser.add_argument("--duration", type=int, default=400, help="Frame duration in ms")
    parser.add_argument("--resize", type=parse_resize, help="Resize images to WIDTHxHEIGHT (e.g., 500x500)")
    parser.add_argument("--fade-steps", type=int, default=5, help="Number of fade frames between images")
    args = parser.parse_args()
    create_gif_with_quotes(
        folder=args.folder,
        output_path=args.output,
        duration=args.duration,
        resize=args.resize,
        fade_steps=args.fade_steps
    )
