from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime

# Settings
text = "CONFIDENTIAL"
date = datetime.now().strftime("%Y%m%d")
font_size = 100
opacity = 100  # 0 to 255 (100 is subtle)
color = (128, 128, 128, opacity) # Gray

# Create image context
# Make a large canvas to ensure text fits when rotated
img = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Load default font (or specific path if you have one)
try:
    font = ImageFont.truetype("Arial.ttf", font_size)
except:
    font = ImageFont.load_default()

# Calculate text size and position
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (1000 - text_width) / 2
y = (1000 - text_height) / 2

# Draw Text
draw.text((x, y), text, fill=color, font=font)

# Draw date below the confidential watermark
date_text = date
date_font_size = int(font_size)
try:
    date_font = ImageFont.truetype("Arial.ttf", date_font_size)
except:
    date_font = ImageFont.load_default()
date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
date_width = date_bbox[2] - date_bbox[0]
gap = 20  # pixels between main text and date
date_x = (1000 - date_width) / 2
date_y = y + text_height + gap
draw.text((date_x, date_y), date_text, fill=color, font=date_font)

# Rotate
img = img.rotate(45, expand=1)

# Crop to content (removes excess transparent space)
bbox = img.getbbox()
img = img.crop(bbox)

# Save
img.save("watermark.png", "PNG")
print("Watermark saved as watermark.png")
