from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


def add(img,top_line_value,bottom_line_value):
	#img = Image.open("source-0.png")
	draw = ImageDraw.Draw(img)
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("Acme-Regular.ttf", 46)
	# draw.text((x, y),"Sample Text",(r,g,b))
	draw.text((250, 20),top_line_value,(0,0,0),font=font)
	draw.text((250, 280),bottom_line_value,(0,0,0),font=font)
	#img.save('sample-out.png')
	return img
