from PIL import Image as im
from PIL import ImageDraw, ImageFont

img_width = 380
img_height = 380
img = im.new('RGB', (img_width, img_height), color='black')
draw = ImageDraw.Draw(img)
text = "Tumor not found !"
font = ImageFont.truetype('./src/gui/arial.ttf', size=30)  # You can choose any font you like and set the size of the text
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
x, y = (img.width - text_width) // 2, (img.height - text_height) // 2
draw.text((x, y), text, fill='white', font=font)
path = './tmp/error_image.png'
img.save(path)