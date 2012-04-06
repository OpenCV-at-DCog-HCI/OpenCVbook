__author__ = 'hutchins'


#A simple module to read a video file from disk and play it.

from cv import NamedWindow, CaptureFromFile, QueryFrame, WaitKey, ShowImage, DestroyWindow

def playVideo(source):
    """ A simple function that reads frames from a video file source and displays them
    in a window. """

    NamedWindow( "Example2")  # Create a window in which the video frames can be shown
    cap = CaptureFromFile(source)  # Create a video capture object for the source from which frames will be read
    frame = QueryFrame(cap) #  Get the first frame of video

    while frame:                       # Exit when there are no more frames in the video file
        ShowImage("Example2", frame)    # Display the frame
        c = WaitKey(33)                 # Wait for user input.  Also wait 33 ms between frames for 30Hz video
        if c == 27 : break            # If the user types the <esc> key, exit the loop
        frame = QueryFrame(cap)         # Get another frame

    DestroyWindow( "Example2" )  # Close the display window object

if __name__ == "__main__":
    #  Use a path name to a video file on your own computer
    fileName = "/Users/hutchins/Documents/research/animalCog/dolphins/video/PoolCam.mov"

    playVideo(fileName)