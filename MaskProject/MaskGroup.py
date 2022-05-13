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
        self.maskImage = None
        self.maskArray = None

    def addMask(self, newMask):
        self.maskList.append(newMask)
        self.refreshMask()
        #print("Added " + newMask.maskName)

    def removeMask(self, delMask):
        self.maskList.remove(delMask)
        if len(self.maskList) > 0:
            self.refreshMask()

    def refreshMask(self):
        self.maskArray = np.copy(self.maskList[0].maskTrueFalse)
        self.maskImage = np.copy(self.maskList[0].maskBlackWhite)

        if len(self.maskList) > 1:
            for x in range(1, len(self.maskList)):
                self.maskArray = np.where(self.maskList[x].maskTrueFalse == True, True, self.maskArray)
                self.maskImage = np.where(self.maskList[x].maskTrueFalse == True, self.maskList[x].maskBlackWhite, self.maskImage)