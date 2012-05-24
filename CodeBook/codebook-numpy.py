'''
Created on Apr 25, 2012

@author: Whitney Friedman & Richard Tibbles

4/26 1:08: Added learnBackground & preamble (may not all function yet)
4/26 5:35: Added lots of functions; almost complete (to do: make it run)
4/27 9:52: Did a bit of debugging. changes to findForeground - possing codeBook(bgCodeBooks)
something still to solve (TypeError: can only concatenate tuple (not "int") to tuple) in learnHigh/learnLow
in codeBook init
5/18 11:00 Reconfiguring to use numpy arrays instead of dicts to make data structures more consistent with OpenCV (and possibly faster?)
'''


from cv import CaptureFromFile, QueryFrame, CreateImage, GetSize, IPL_DEPTH_8U, GetCaptureProperty,\
    CreateVideoWriter, CV_CAP_PROP_FPS, WriteFrame, ShowImage, DestroyWindow, Copy, CV_CAP_PROP_FOURCC
    
import numpy as np

def findForeground(bgCodeBooks,dataVideo, videoOut):
    cap = CaptureFromFile(dataVideo)
    frame = QueryFrame(cap)
    fgFrame = CreateImage(GetSize(frame), IPL_DEPTH_8U, 3)
    Mask = CreateImage(GetSize(frame), IPL_DEPTH_8U, 3)
    fourcc=int(GetCaptureProperty(cap,CV_CAP_PROP_FOURCC))
    #fourcc=828601953
    #fourcc=877677894
    writer = CreateVideoWriter(videoOut,fourcc,GetCaptureProperty(cap,CV_CAP_PROP_FPS),GetSize(frame),is_color=1)

    while frame:

        for row in range(0,frame.height):
            for column in range(0,frame.width):
                fgPixel = frame[row,column]
                codeBook=bgCodeBooks[row,column]
                Mask[row,column]=tuple([codeBook.checkForeground(fgPixel)]*3)

        Copy(Mask,fgFrame)
        print fgFrame
        #ShowImage("Foreground View", fgFrame)
        WriteFrame(writer,fgFrame)
        print "frame Written to file"
        frame = QueryFrame(cap)

    #DestroyWindow("regionView")
    print 'File written to: ',videoOut



def learnBackground(background):
    cap = CaptureFromFile(background)
    frame = QueryFrame(cap)
    # initialize all the codeBooks in the first frame. then run a loop for the rest.
    codeBooks = cBInit(np.asarray(frame[:,:]))
    print "initial codeBook created"



    # run through rest of frames...
    frame = QueryFrame(cap)
    f = 1
    while frame:
        codeBooks = cBUpdate(codeBooks,np.asarray(frame[:,:]))

        print 'codeBooks for frame', f ,'learned'
        frame = QueryFrame(cap)
        f += 1


    return codeBooks
    print "finished creating codeBooks!"

def codeBookInitialize(pixel):
    return codeBook(pixel)
    
cBInit = np.frompyfunc(codeBookInitialize,1,1)
    
def codeBookUpdate(codebook,pixel):
    return codebook.update_codebook(pixel)
    
cBUpdate = np.frompyfunc(codeBookUpdate,2,1)

class codeBook():

    def __init__(self,pixel,cbBounds=10,numChannels=3):
        self.cbBounds = [cbBounds]*numChannels
        cbBounds=self.cbBounds
        self.numChannels = numChannels
        self.codeElements=[]
        self.t = 0
        pixel = list(pixel)
        #wf added until next comments...still doesn't work. 
        learnHigh = [0]*numChannels
        learnLow = [0]*numChannels

        for n in range (0,numChannels):
            if pixel[n]+cbBounds[n] < 256:
                learnHigh[n] = pixel[n]+cbBounds[n]
            else: learnHigh[n]=255

            if pixel[n]-cbBounds[n] > -1:
                learnLow[n]=pixel[n]-cbBounds[n]
            else:learnLow[n] = 0
            #learnHigh = [x + cbBounds if x + cbBounds < 256 else 255 for x in pixel]
            #learnLow = [x - cbBounds if x - cbBounds > -1 else 0 for x in pixel]
        self.codeElements.append(ce(learnHigh,learnLow,pixel,pixel,self.t))

    def update_codebook (self,pixel):
        self.t += 1
        cbBounds = self.cbBounds
        numChannels = self.numChannels
        celist = self.codeElements
        numEntries = len(celist)
        pixel = list(pixel)
        high = [0]*numChannels
        low = [0]*numChannels
        newEntry = True
        #Set high and low for this pixel, make sure they are not outside the bounds of 0 and 255
        for n in range(0,numChannels):
            high[n] = pixel[n]+cbBounds[n]
            if high[n] > 255:
                high[n] = 255

            low[n] = pixel[n]-cbBounds[n]
            if low[n] < 0:
                low[n] = 0


        for i in range(0,numEntries):
            matchChannel = 0
            for n in range(0,numChannels):
                if celist[i].learnLow[n] <= pixel[n] and pixel[n] <= celist[i].learnHigh[n]:
                    matchChannel+=1
            if matchChannel == numChannels:
                celist[i].t_last_update == self.t
                for n in range(0,numChannels):
                    if celist[i].max[n] < pixel[n]:
                        celist[i].max[n] = pixel[n]
                        if celist[i].learnHigh[n] < high[n]:
                            celist[i].learnHigh[n] += 1

                    elif celist[i].min[n] > pixel[n]:
                        celist[i].min[n] = pixel[n]
                        if celist[i].learnLow[n] < low[n]:
                            celist[i].learnLow[n] += 1
                newEntry=False
                break

        for s in range(0,numEntries):
            negRun = self.t - celist[s].t_last_update
            if celist[s].stale < negRun:
                celist[s].stale = negRun

        if newEntry:
            celist.append(ce(high,low,pixel,pixel,self.t))

    def clear_stale_entries(self):
        celist = self.codeElements
        numEntries = len(celist)

        staleThresh = self.t/2
        keep =[0]*numEntries
        keepCnt = 0

        # mark stale entries for destruction
        for i in range(0,numEntries):
            if celist[i].stale > staleThresh:
                keep[i] =0 # mark for destruction
            else:
                keep[i] = 1
                keepCnt += 1 # mark to keep

        # keep the good entries; destroy stale
        self.t = 0
        codeElements = codeElements[keep] #returns values if keep = 1; otherwise stale entry 'deleted'

    def checkForeground(self,fgPixel,modMin=10, modMax=10):
        #cbBounds = self.cbBounds
        numChannels = self.numChannels
        minMod = [modMin]*numChannels
        maxMod = [modMax]*numChannels
        celist = self.codeElements
        numEntries = len(celist)
        fgPixel=list(fgPixel)

        for i in range(0,numEntries):
            matchChannel = 0
            for n in range(0,numChannels):
                if celist[i].min[n]-minMod[n] <= fgPixel[n] and fgPixel[n] <= celist[i].max[n]+maxMod[n]:
                    matchChannel+=1
                else: break
            if matchChannel == numChannels:
                return 255
        return 0



class ce:
    def __init__(self,learnHigh,learnLow,max,min,t_last_update):
        self.stale = 0
        self.learnHigh = learnHigh
        self.learnLow = learnLow
        self.max = list(max)
        self.min = list(min)
        self.t_last_update = t_last_update



if __name__=="__main__":

    learningVideo = "dolphinBackgroundShort_ROI"
    dataVideo = "dolphinAerialShort_ROI"
    output = "/Users/Whitney/Temp/AerialClips/dolphinBackground_codebook2"


    bgCodeBooks=learnBackground(learningVideo)
    findForeground(bgCodeBooks,dataVideo,output)