from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# Adds text with "meme font" in the top and bottom on the frames of a gif
def add(img,top_line_value,bottom_line_value,width,height):
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("impact.ttf", 46)
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

	fillcolor = "white"
	shadowcolor = "black"

	x = middleTop
	y = 20 
	text = top_line_value

	# thin border
	draw.text((x-1, y), text, font=font, fill=shadowcolor)
	draw.text((x+1, y), text, font=font, fill=shadowcolor)
	draw.text((x, y-1), text, font=font, fill=shadowcolor)
	draw.text((x, y+1), text, font=font, fill=shadowcolor)

	# thicker border
	draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
	draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
	draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
	draw.text((x+1, y+1), text, font=font, fill=shadowcolor)

	# now draw the text over it
	draw.text((x, y), text, font=font, fill=fillcolor)

	x = middleBot
	y = height - 70
	text = bottom_line_value

	# thin border
	draw.text((x-1, y), text, font=font, fill=shadowcolor)
	draw.text((x+1, y), text, font=font, fill=shadowcolor)
	draw.text((x, y-1), text, font=font, fill=shadowcolor)
	draw.text((x, y+1), text, font=font, fill=shadowcolor)

	# thicker border
	draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
	draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
	draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
	draw.text((x+1, y+1), text, font=font, fill=shadowcolor)

	# now draw the text over it
	draw.text((x, y), text, font=font, fill=fillcolor)

	return img
