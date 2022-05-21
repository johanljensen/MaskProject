from MaskSettings import MaskSettings
import numpy as np

class Mask:

    def __init__(self, array, name, maskClass):
        self.maskSettings = MaskSettings()
        self.maskName = name
        self.maskClass = maskClass
        #self.maskBlackWhite = img

        self.maskTrueFalse = array
        where = np.where(array)
        xMin, yMin, zMin = np.amin(where, axis=1)
        xMax, yMax, zMax = np.amax(where, axis=1)

        self.minX = xMin
        self.minY = yMin
        self.maxX = xMax
        self.maxY = yMax

        #self.maskImageBounded = array[self.minX:self.maxX, self.minY:self.maxY]
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