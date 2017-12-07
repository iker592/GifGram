from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 



import  os

x, y = 10, 10

fname1 = "test.png"
im = Image.open(fname1)
pointsize = 46
fillcolor = "white"
shadowcolor = "black"

text = "HI THERE"


draw = ImageDraw.Draw(im)
font = ImageFont.truetype("impact.ttf", pointsize)

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

fname2 = "test.png"
im.save(fname2)



