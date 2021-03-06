import numpy as np
import ClassDict
from Mask import Mask
from MaskGroup import MaskGroup


class MaskDetector:

    def DetectMasks(self, imagePath):
        mask_array = np.load(imagePath + 'Image_mask.npy')
        class_array = np.load(imagePath + 'class_array.npy')
        num_instances = mask_array.shape[0]
        mask_array = np.moveaxis(mask_array, 0, -1)

        classDict = ClassDict

        maskList = []
        classList = []
        uniqueClasses = []

        for i in range(num_instances):
            j = class_array[i] + 1

            maskName = "" + str(i) + " - " + classDict.coco_dict[j]
            maskTrueFalse = mask_array[:, :, i:(i + 1)]
            #maskBlackWhite = np.zeros_like(maskTrueFalse, dtype=np.uint8)
            #maskBlackWhite = np.where(maskTrueFalse == True, 255, maskBlackWhite)

            maskList.append(Mask(maskTrueFalse, maskName, classDict.coco_dict[j]))
            #cv2.imshow("hey:" + str(i), maskBlackWhite)

            if classDict.coco_dict[j] not in uniqueClasses:
                uniqueClasses.append(classDict.coco_dict[j])

        for uClass in uniqueClasses:
            maskGroup = MaskGroup(uClass)
            for mask in maskList:
                if mask.maskClass == uClass:
                    maskGroup.AddMask(mask)
                    #print("Added mask of class: " + mask.maskClass + " to group of class: " + uClass)
            classList.append(maskGroup)

        return maskList, classList
