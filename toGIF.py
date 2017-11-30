import imageio
#filenames = ["source-0.png","source-1.png","source-2.png"]

def gifIt(filenames):
	images = []
	for filename in filenames:
	    images.append(imageio.imread(filename))
	imageio.mimsave('newGIF.gif', images)