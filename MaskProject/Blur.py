import cv2
import numpy as np

class Blur:

    def BlurFilter(self, baseImage, mask, imagePath, str, background, apply):
        if (apply):
            blur = cv2.blur(baseImage, (str, str))
            if background:
                blur = np.where(mask.maskTrueFalse == False, blur, baseImage)
            else:
                blur = np.where(mask.maskTrueFalse == True, blur, baseImage)
            cv2.imwrite(imagePath + 'p6_maskedit.png', blur)
        else:
            cv2.imwrite(imagePath + 'p6_maskedit.png', baseImage)