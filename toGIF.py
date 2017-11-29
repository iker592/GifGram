import imageio
filenames = ["source-0.png","source-1.png","source-2.png"]
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('movie.gif', images)