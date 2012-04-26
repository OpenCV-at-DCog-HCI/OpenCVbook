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