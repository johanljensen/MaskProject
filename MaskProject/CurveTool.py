import cv2
import numpy as np
import matplotlib.pyplot as pl

class CurveTool:

    def ConvertValue(self, value, val1, val2, val3):
        look_up_table = np.zeros((256, 1), dtype='uint8')
        for i in range(256):
            look_up_table[i][0] = (float(val1/1000000) * i ** 3) + (float(val2/1000) * i ** 2) + (float(val3) * i)
            lutImg = np.zeros_like(value)
            lut = cv2.LUT(value, look_up_table, lutImg)
        return lut

    def ApplyColorCurve(self, val1, val2, val3, channel, image):
        if val1 < -10:
            val1 = -10
        if val1 > 10:
            val1 = 10
        if val2 < -10:
            val2 = -10
        if val2 > 10:
            val2 = 10
        if val3 < -10:
            val3 = -10
        if val3 > 10:
            val3 = 10

        fig = pl.figure()
        x = np.arange(0, 255, 0.1)
        y = (float(val1 / 1000000) * x ** 3) + (float(val2 / 1000) * x ** 2) + (
                    float(val3) * x / 100)
        pl.plot(x, y)
        fig.savefig('imageData/plot.png')
        pl.close(fig)
        #newImage = cv2.imread(image.baseImagePath)
        b, g, r = cv2.split(image)
        if channel == "Blue":
            b = np.clip(self.ConvertValue(b, val1, val2, val3), 0, 255)
        elif channel == "Green":
            g = np.clip(self.ConvertValue(g, val1, val2, val3), 0, 255)
        elif channel == "Red":
            r = np.clip(self.ConvertValue(r, val1, val2, val3), 0, 255)
        elif channel == "All":
            b = np.clip(self.ConvertValue(b, val1, val2, val3), 0, 255)
            g = np.clip(self.ConvertValue(g, val1, val2, val3), 0, 255)
            r = np.clip(self.ConvertValue(r, val1, val2, val3), 0, 255)
        else:
            return
        newImg = cv2.merge((b, g, r))
        return newImg