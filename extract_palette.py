from PIL import Image

img_path = r"C:\Users\s7gma\PycharmProjects\echo_game\assets\images\chasm-32x.png"

img = Image.open(img_path).convert('RGB')

colors =  []
for x in range(img.width):
    color = img.getpixel((x, img.height // 2))
    if color not in colors:
        colors.append(color)

print("LEVEL_COLORS = [")
for color in colors:
    print(f"    {color},")
print("]")
print(f"\nExtracted {len(colors)} colors from  {img_path}")
