'''
Created on Apr 25, 2012

@author: Whitney Friedman & Richard Tibbles

4/26 1:08: Added learnBackground & preamble (may not all function yet)
'''


from cv import CaptureFromFile, QueryFrame


def learnBackground(background):
    cap = CaptureFromFile(background)
    frame = QueryFrame(cap)
    codeBooks=[]

    # initialize all the codeBooks in the first frame. then run a loop for the rest.

    for row in range(0,frame.height):
        codeBooks.append([])
        for column in range (0,frame.width):
            pixel = frame[row,column]
            codeBooks.append(codeBook(pixel))

    # run through rest of frames...
    frame = QueryFrame(cap)
    while frame:
        for row in range(0,frame.height):
            for column in range (0,frame.width):
                codebook=codeBooks[row][column]
                pixel = frame[row,column]
                codebook.updateCodebook(pixel)

        frame = QueryFrame(cap)

    return codeBooks



class codeBook:
    
    def __init__(self,pixel,cbBounds=10,numChannels=3):
        self.cbBounds = [cbBounds]*numChannels
        self.numChannels = numChannels
        self.codeElements=[]
        self.t = 0
        pixel = list(pixel)
        learnHigh = [x + cbBounds if x + cbBounds < 256 else 255 for x in pixel]
        learnLow = [x - cbBounds if x - cbBounds > -1 else 0 for x in pixel]
        self.codeElements.append(ce(learnHigh,learnLow,pixel,pixel,self.t))
    
    def update_codebook (self,pixel):
        self.t += 1
        cbBounds = self.cbBounds
        numChannels = self.numChannels
        celist = self.codeElements
        numEntries = len(celist)
        pixel = list(pixel)
        high = []*numChannels
        low = []*numChannels
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
                break
        for s in range(0,numEntries):
            negRun = self.t - celist[s].t_last_update
            if celist[s].stale < negRun:
                celist[s].stale = negRun
        if i==numEntries:
            celist.append(ce(high,low,pixel,pixel,self.t))
            


class ce:
    def __init__(self,learnHigh,learnLow,max,min,t_last_update):
        self.stale = 0
        self.learnHigh = learnHigh
        self.learnLow = learnLow
        self.max = max
        self.min = min
        self.t_last_update = t_last_update



if __name__=="__main__":

    learningVideo = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort_ROI"
    dataVideo = "/Users/Whitney/Temp/AerialClips/dolphinAerialShort_ROI"
    output = "/Users/Whitney/Temp/AerialClips/dolphinBackground_codebook"


    learnBackground(learningVideo)