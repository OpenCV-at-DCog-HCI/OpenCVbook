__author__ = 'jkarnows'

from cv import LoadImage, NamedWindow, ShowImage, CreateImage, Smooth, GetSize, IPL_DEPTH_8U, CV_GAUSSIAN, WaitKey, DestroyWindow

def smoothImage(imagefile):

    image = LoadImage(imagefile)        # Converts image to correct filetype for cv

    NamedWindow("Original Image")       # Opens two windows for file comparison
    NamedWindow("Smoothed Image")

    ShowImage("Original Image",image)   # Shows original image

    smooth = CreateImage(GetSize(image),IPL_DEPTH_8U,3) # Creates a variable to store a new image
    Smooth(image,smooth,CV_GAUSSIAN,3,3)                # Uses gaussian to smooth image and save into smooth variable
    ShowImage("Smoothed Image",smooth)  # Shows altered image

    WaitKey(0)
    DestroyWindow("Original Image")     # Closes the two windows
    DestroyWindow("Smoothed Image")

if __name__ == "__main__":
    path = "dolphin.jpg"                # Use correct filepath on your computer
    smoothImage(path)                   # Test out function with a dolphin image