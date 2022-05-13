import cv2
import numpy as np

class Blur:

    def BlurFilter(self, image, mask, str, background, apply):
        if (apply):
            blur = cv2.blur(image, (str, str))
            if background:
                blur = np.where(mask.maskTrueFalse == False, blur, image)
            else:
                blur = np.where(mask.maskTrueFalse == True, blur, image)
            cv2.imwrite('images/edit.png', blur)
        else:
            cv2.imwrite('images/edit.png', image)