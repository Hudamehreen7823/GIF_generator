import os
import argparse
import random
from PIL import Image, ImageDraw, ImageFont

# List of random quotes
QUOTES = [
    "Believe in yourself!",
    "Shine bright ✨",
    "Keep going 💪",
    "Dream big 💭",
    "Stay curious 🔍",
    "Create magic 🌟",
    "Make it happen!",
    "Never give up!",
    "Push your limits 🚀"
]


def add_sparkle_text(image, text, font_path="Pluretta Vintage DEMO VERSION", font_size=50):
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(" Freestyle Script font not found. Using default font.")
        font = ImageFont.load_default()

    # Center text
    text_width, text_height = draw.textsize(text, font=font)
    img_width, img_height = image.size
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2

    # Sparkle effect: shadow outline with vibrant colors
    colors = ["#FF69B4", "#FFD700", "#ADFF2F", "#00FFFF", "#FF4500"]
    for dx, dy in [(-2, -2), (2, 2), (-2, 2), (2, -2)]:
        draw.text((x + dx, y + dy), text, font=font, fill=random.choice(colors))

    # Main text
    draw.text((x, y), text, font=font, fill=random.choice(colors))
    return image

def create_fade_transition(img1, img2, steps=5):
    return [Image.blend(img1, img2, i / (steps + 1)).convert("RGBA") for i in range(1, steps + 1)]

def create_gif_with_sparkle_quotes(folder, output_path, duration=500, resize=None, fade_steps=5):
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
        img = add_sparkle_text(img, quote)

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
    parser = argparse.ArgumentParser(description="Create a sparkle GIF with random quotes and fade transitions.")
    parser.add_argument("folder", help="Folder containing images")
    parser.add_argument("output", help="Output GIF file path")
    parser.add_argument("--duration", type=int, default=400, help="Frame duration (ms)")
    parser.add_argument("--resize", type=parse_resize, help="Resize to WIDTHxHEIGHT, e.g., 500x500")
    parser.add_argument("--fade-steps", type=int, default=5, help="Number of fade transition steps")
    
    args = parser.parse_args()

    create_gif_with_sparkle_quotes(
        folder=args.folder,
        output_path=args.output,
        duration=args.duration,
        resize=args.resize,
        fade_steps=args.fade_steps
    )
