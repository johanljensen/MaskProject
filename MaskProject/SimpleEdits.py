import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

class SimpleEdits:

    def DrawBrightness(self, brightnessValue, image):

        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h_values, s_values, v_values = cv2.split(hsvImage)

        if brightnessValue > 0:
            limit = 255 - brightnessValue
            v_values[v_values > limit] = 255
            v_values[v_values <= limit] += brightnessValue
        else:
            limit = 0 + abs(brightnessValue)
            v_values[v_values < limit] = 0
            # This line of code cannot add negatives, so we force positive and subtract
            v_values[v_values >= limit] -= abs(brightnessValue)

        mergeHSV = cv2.merge((h_values, s_values, v_values))
        newImg = cv2.cvtColor(mergeHSV, cv2.COLOR_HSV2BGR)
        return newImg

    def DrawSaturation(self, saturationValue, image):

        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h_values, s_values, v_values = cv2.split(hsvImage)

        if saturationValue > 0:
            limit = 255 - saturationValue

            s_values[s_values > limit] = 255
            s_values[s_values <= limit] += saturationValue
        else:
            limit = 0 + abs(saturationValue)
            s_values[s_values < limit] = 0
            # This line of code cannot add negatives, so we force positive and subtract
            s_values[s_values >= limit] -= abs(saturationValue)

        mergeHSV = cv2.merge((h_values, s_values, v_values))
        newImg = cv2.cvtColor(mergeHSV, cv2.COLOR_HSV2BGR)
        return newImg