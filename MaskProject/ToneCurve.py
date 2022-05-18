import cv2
import numpy as np
import matplotlib.pyplot as plt


class ToneCurve:

    def DrawHistogram(self, filterName, currentGraphic):
        # image = cv2.imread('input.jpg')
        image = currentGraphic.ravel()
        #print(image.size)
        counts, bins = np.histogram(image, bins=256)
        normalizer = (256 / max(counts)) * counts
        #print(normalizer)
        #print(max(normalizer))
        #print(sum(counts))
        #print(max(counts))
        plt.hist(bins[0:-1], bins, weights=normalizer, color="gray")

        # Define X and Y variable data
        x = np.arange(0, 256)
        y = x.copy()

        if filterName == "Negative reversal":
            y = 255 - x

        elif filterName == "Line curve":
            for i in range(len(x)):
                if i < 256 / 2:
                    y[i] = x[i] * 2
                else:
                    y[i] = 255

        elif filterName == "S-Curve":
            y = 255 * (np.sin(np.pi * (x/255 - 1/2)) + 1) / 2

        elif filterName == "Solarization":
            y = (np.sin(3 * np.pi * (x / 255 + 1 / 2)) + 1) * 255 / 2

        elif filterName == "Posterization":
            step = 4
            split = int(256 / (step - 1))
            up = int(256 / step)
            for i in range(256):
                if np.trunc(i / up) * split >= 255:
                    y[i] = 255
                else:
                    y[i] = np.trunc(i / up) * split

        plt.plot(x, y, color="black")
        plt.xlabel("Input pixels")  # add X-axis label
        plt.ylabel("Output pixels")  # add Y-axis label
        plt.title("Tone curve")  # add title
        plt.grid(True)
        #plt.show()
        plt.savefig("imageData/toneCurvePlot")
        plt.close()

    def ApplyFilter(self, filterName, currentGraphic):

        filteredImage = currentGraphic

        if filterName == "Negative reversal":
            filteredImage = self.Reversal(currentGraphic)
        elif filterName == "S-Curve":
            filteredImage = self.S_ToneCurve(currentGraphic)
        elif filterName == "Line curve":
            filteredImage = self.LineCurve(currentGraphic)
        elif filterName == "Solarization":
            filteredImage = self.Solarization(currentGraphic)
        elif filterName == "Posterization":
            filteredImage = self.Posterization(currentGraphic)

        cv2.imshow("Filter", filteredImage)

    def Reversal(self, currentGraphic):
        print("Reverse the coloration")
        reversedImage = 255 - currentGraphic
        return reversedImage

    def LineCurve(self, currentGraphic):
        print("Lining the curve")
        look_up_table = np.zeros((256, 1), dtype='uint8')
        for i in range(256):
            if i < 256 / 2:
                look_up_table[i][0] = i * 2
            else:
                look_up_table[i][0] = 255
        return cv2.LUT(currentGraphic, look_up_table)

    def S_ToneCurve(self, currentGraphic):
        print("S_Curving")
        look_up_table = np.zeros((256,1), dtype='uint8')
        for i in range(256):
            look_up_table[i][0] = 255 * (np.sin(np.pi * (i/255 - 1/2)) + 1) / 2
        return cv2.LUT(currentGraphic, look_up_table)

    def Solarization(self, currentGraphic):
        print("Solar power")
        look_up_table = np.zeros((256, 1), dtype='uint8')
        for i in range(256):
            look_up_table[i][0] = (np.sin(3 * np.pi * (i / 255 + 1 / 2)) + 1) * 255 / 2
        return cv2.LUT(currentGraphic, look_up_table)

    def Posterization(self, currentGraphic):
        print("Original poster")
        step = 4
        look_up_table = np.zeros((256, 1), dtype='uint8')
        split = int(256 / (step - 1))
        up = int(256 / step)
        for i in range(256):
            if np.trunc(i / up) * split >= 255:
                look_up_table[i][0] = 255
            else:
                look_up_table[i][0] = np.trunc(i / up) * split
        return cv2.LUT(currentGraphic, look_up_table)
