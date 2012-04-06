__author__ = 'jkarnows'

from cv import *

def doPyrDown(image, filter=CV_GAUSSIAN_5x5):
    oldsize = GetSize(image)
    if (oldsize[0] % 2 == 1) and (oldsize[1] % 2 == 1):
        oldsize = tuple([oldsize[0]-1,oldsize[1]-1])
    elif oldsize[0] % 2 == 1:
        oldsize = tuple([oldsize[0]-1,oldsize[1]])
    elif oldsize[1] % 2 == 1:
        oldsize = tuple([oldsize[0],oldsize[1]-1])
    else:
        pass
    newsize = tuple([oldsize[0]/2,oldsize[1]/2])
    halvedImage = CreateImage(newsize,image.depth,image.nChannels)
    PyrDown(image,halvedImage)
    return halvedImage

def doCanny(image, lowThresh, highThresh, aperture):
    if image.nChannels != 1:
        return
    cannyImage = CreateImage(GetSize(image),image.depth,1)
    Canny(image,cannyImage,lowThresh,highThresh,aperture)
    return cannyImage

def smallCanny(imagefile):
    img = LoadImage(imagefile)
    out = doPyrDown(img)
    out = doPyrDown(out)
    out = doCanny(out,10,100,3) # This seems to give me empty image right now. Thoughts?!

    NamedWindow("Original Image")       # Opens two windows for file comparison
    NamedWindow("Altered Image")

    ShowImage("Original Image",img)   # Shows original image
    ShowImage("Altered Image",out)  # Shows altered image

    WaitKey(0)
    DestroyWindow("Original Image")     # Closes the two windows
    DestroyWindow("Smoothed Image")

if __name__ == "__main__":
    path = "../dolphin.jpg"
    smallCanny(path)                                 # Test out function with a dolphin image