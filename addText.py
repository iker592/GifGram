from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


def add(img,top_line_value,bottom_line_value,width,height):
	#img = Image.open("source-0.png")
	draw = ImageDraw.Draw(img)
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("impact.ttf", 46)
	#font = ImageFont.truetype('arial.ttf', 46)
	ascent, descent = font.getmetrics()
	(widthy, baseline), (offset_x, offset_y) = font.font.getsize(top_line_value)
	(widthy2, baseline2), (offset_x2, offset_y2) = font.font.getsize(bottom_line_value)

	if top_line_value != "":
		blackRectangleTop = font.getmask(top_line_value).getbbox()
	else:
		blackRectangleTop =(0,0,0)

	if bottom_line_value !="":
		blackRectangleBot = font.getmask(bottom_line_value).getbbox()
	else:
		blackRectangleBot=(0,0,0)

	middleTop = width/2 -blackRectangleTop[2]/2
	middleBot = width/2 -blackRectangleBot[2]/2

	draw.text(( middleTop , 20),top_line_value,font=font)
	draw.text(( middleBot , 280),bottom_line_value,font=font)
	#img.save('sample-out.png')
	return img
