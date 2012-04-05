__author__ = 'jkarnows'

## Example 2-1. A simple OpenCV program that loads an image from disk and displays it on the screen

from cv import LoadImage, NamedWindow, ShowImage, WaitKey, DestroyWindow, CV_WINDOW_AUTOSIZE

def openImage(image):
    """
    A function that takes a filename string as input (e.g. "dolphin.jpg") and displays the image on the screen.
    """
    img = LoadImage(image)                          # Loads image
    NamedWindow("Example1", CV_WINDOW_AUTOSIZE)     # Creates a window on screen
    ShowImage("Example1",img)                       # Displays the image in the window
    WaitKey(0)                                      # Waits until a key is pressed (or window is closed)
    DestroyWindow("Example1")                       # Removes the window from the screen

openImage("dolphin.jpg")                            # Test out function with a dolphin image