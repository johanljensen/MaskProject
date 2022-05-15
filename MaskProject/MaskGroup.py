import cv2
import numpy as np

from Mask import Mask
from MaskSettings import MaskSettings

class MaskGroup():

    def __init__(self, name, maskClass):
        self.maskList = []
        self.maskSettings = MaskSettings()
        self.groupName = name
        self.maskClass = maskClass
        self.maskBlackWhite = None
        self.maskTrueFalse = None

    def getMasks(self):
        print(len(self.maskList))
        return self.maskList

    def addMask(self, newMask):
        self.maskList.append(newMask)
        self.refreshMask()
        #print("Added " + newMask.maskName)

    def removeMask(self, delMask):
        self.maskList.remove(delMask)
        if len(self.maskList) > 0:
            self.refreshMask()

    def refreshMask(self):
        self.maskTrueFalse = np.copy(self.maskList[0].maskTrueFalse)
        self.maskBlackWhite = np.copy(self.maskList[0].maskBlackWhite)

        if len(self.maskList) > 1:
            for x in range(1, len(self.maskList)):
                self.maskTrueFalse = np.where(self.maskList[x].maskTrueFalse == True, True, self.maskTrueFalse)
                self.maskBlackWhite = np.where(self.maskList[x].maskTrueFalse == True, self.maskList[x].maskBlackWhite, self.maskBlackWhite)