from MaskSettings import MaskSettings
import numpy as np

class Mask:

    def __init__(self, array, img, name, maskClass):
        self.maskSettings = MaskSettings()
        self.maskName = name
        self.maskClass = maskClass
        self.maskBlackWhite = img
        self.maskTrueFalse = array

        where = np.where(img)
        x1, y1, z1 = np.amin(where, axis=1)
        x2, y2, z2 = np.amax(where, axis=1)

        self.minX = x1
        self.minY = y1
        self.maxX = x2
        self.maxY = y2

        self.maskImageBounded = img[self.minX:self.maxX, self.minY:self.maxY]
        #cv2.imshow(name, self.boundedImage)

    def GetMasks(self):
        return [self]

    def SetColorValues(self, value1, value2, value3, colorChannel):
        self.maskSettings.colorCurve1 = value1
        self.maskSettings.colorCurve2 = value2
        self.maskSettings.colorCurve3 = value3
        self.maskSettings.colorChannel = colorChannel

    def SetToneCurveFilter(self, filterName):
        self.maskSettings.toneCurve = filterName