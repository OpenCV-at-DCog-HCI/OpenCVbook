__author__ = 'jkarnows'

from cv import *

class Scroller:

    def __init__(self):
        self.g_slider_position = 0
        self.g_capture = None

    def onTrackbarSlide(self,pos):
        """
        Defines what the Slider does when moved
        """
        SetCaptureProperty(self.g_capture, CV_CAP_PROP_POS_FRAMES, pos)

    def main(self,videofile):
        NamedWindow( "Example3", CV_WINDOW_AUTOSIZE)    # Opens a new window
        self.g_capture = CaptureFromFile(videofile);    # Captures video from file
        frame = QueryFrame(self.g_capture)              # Grabs the first image from the video
        frames = GetCaptureProperty(self.g_capture, CV_CAP_PROP_FRAME_COUNT)    # Gets the number of frames
        if frames!= 0:                                  # Creates Scrollbar on window
            CreateTrackbar("Position", "Example3", self.g_slider_position, int(frames), self.onTrackbarSlide)

        while frame:                        # Exit when there are no more frames in the video file
            ShowImage("Example3", frame)    # Display the frame
            c = WaitKey(33)                 # Wait for user input.  Also wait 33 ms between frames for 30Hz video
            if c == 27 : break              # If the user types the <esc> key, exit the loop
            frame = QueryFrame(self.g_capture)         # Get another frame

        DestroyWindow("Example3")  # Close the display window object

if __name__ == "__main__":
    path = "dolphins.avi"
    scroller = Scroller()
    scroller.main(path)                                 # Test out function with a dolphin video