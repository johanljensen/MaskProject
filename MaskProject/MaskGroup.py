import numpy as np

from MaskSettings import MaskSettings

class MaskGroup():

    def __init__(self, name):
        self.maskList = []
        self.maskSettings = MaskSettings()
        self.maskName = name
        self.maskBlackWhite = None
        self.maskTrueFalse = None

    def GetMasks(self):
        return self.maskList

    def AddMask(self, newMask):
        self.maskList.append(newMask)
        self.RefreshMask()
        #print("Added " + newMask.maskName)

    def RemoveMask(self, delMask):
        self.maskList.remove(delMask)
        if len(self.maskList) > 0:
            self.RefreshMask()

    def SetColorValues(self, value1, value2, value3, colorChannel):
        self.maskSettings.colorCurve1 = value1
        self.maskSettings.colorCurve2 = value2
        self.maskSettings.colorCurve3 = value3
        self.maskSettings.colorChannel = colorChannel

        for mask in self.maskList:
            mask.maskSettings.colorChannel = colorChannel

    def SetToneCurveFilter(self, filterName):
        self.maskSettings.toneCurve = filterName

        for mask in self.maskList:
            mask.maskSettings.toneCurve = filterName

    def RefreshMask(self):
        self.maskTrueFalse = np.copy(self.maskList[0].maskTrueFalse)
        self.maskBlackWhite = np.copy(self.maskList[0].maskBlackWhite)

        if len(self.maskList) > 1:
            for x in range(1, len(self.maskList)):
                self.maskTrueFalse = np.where(self.maskList[x].maskTrueFalse == True, True, self.maskTrueFalse)
                self.maskBlackWhite = np.where(self.maskList[x].maskTrueFalse == True, self.maskList[x].maskBlackWhite, self.maskBlackWhite)