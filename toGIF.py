import imageio
import os

def gifIt(filenames):
	images = []
	for filename in filenames:
	    images.append(imageio.imread(filename))
	imageio.mimsave('newGIF.gif', images)
	#for f in filenames:
		#os.remove(f)