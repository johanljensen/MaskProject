import cv2
import numpy as np
import ClassDict
from Mask import Mask
from MaskGroup import MaskGroup


class MaskSelection:

    def __init__(self):
        self.maskList = []
        self.classList = []
        self.uniqueClasses = []

    def DetectMasks(self, imagePath):

        mask_array = np.load(imagePath + 'Image_mask.npy')
        class_array = np.load(imagePath + 'class_array.npy')
        num_instances = mask_array.shape[0]
        mask_array = np.moveaxis(mask_array, 0, -1)

        classDict = ClassDict

        for i in range(num_instances):
            j = class_array[i] + 1

            maskName = "" + str(i) + " - " + classDict.coco_dict[j]
            maskTrueFalse = mask_array[:, :, i:(i + 1)]
            maskBlackWhite = np.zeros_like(maskTrueFalse, dtype=np.uint8)
            maskBlackWhite = np.where(maskTrueFalse == True, 255, maskBlackWhite)

            self.maskList.append(Mask(maskTrueFalse, maskBlackWhite, maskName, classDict.coco_dict[j]))
            #cv2.imshow("hey:" + str(i), maskBlackWhite)

            if classDict.coco_dict[j] not in self.uniqueClasses:
                self.uniqueClasses.append(classDict.coco_dict[j])

        for uClass in self.uniqueClasses:
            maskGroup = MaskGroup(uClass, uClass)
            for mask in self.maskList:
                if mask.maskClass == uClass:
                    maskGroup.addMask(mask)
                    #print("Added mask of class: " + mask.maskClass + " to group of class: " + uClass)
            self.classList.append(maskGroup)

        return self.maskList, self.classList