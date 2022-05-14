import cv2
import numpy as np
import timeit
from PyQt5.QtGui import QPixmap

from MaskSelection import MaskSelection
from SimpleEdits import SimpleEdits
from CurveTool import CurveTool
from Blur import Blur

class MaskManager:

    def __init__(self):
        print("MaskManager made")

        self.imagePath = 'imageData/Royal Guard/'

        self.baseImage = cv2.imread(self.imagePath + 'input.jpg')
        self.currentImage = self.baseImage.copy()

        self.displayGraphic = None
        self.instanceDropdown = None
        self.classDropdown = None


        self.simpleEdits = SimpleEdits()
        self.curveTool = CurveTool()
        self.blur = Blur()

        self.maskList, self.classList = MaskSelection().DetectMasks(self.imagePath)
        self.groupList = []

        self.selectedMask = None
        self.selectedIsGroup = False

        self.drawTimer = timeit.default_timer()

    def SetUIreferences(self, imageLabel, instanceDropdown, classDropDown):
        self.displayGraphic = imageLabel
        self.instanceDropdown = instanceDropdown
        self.classDropdown = classDropDown

    def SetMaskLists(self):
        self.maskList, self.classList = MaskSelection().DetectMasks(self.imagePath)

        self.instanceDropdown.clear()
        for mask in self.maskList:
            self.instanceDropdown.addItem(mask.maskName)

        self.classDropdown.clear()
        for maskClass in self.classList:
            self.classDropdown.addItem(maskClass.groupName)

        self.selectedMask = self.maskList[0]

    def ImageSelect(self, imageName):
        print("Switched to image: " + imageName)
        self.imagePath = "imageData/" + imageName + "/"
        self.displayGraphic.setPixmap(QPixmap(self.imagePath + "input.jpg"))
        self.baseImage = cv2.imread(self.imagePath + 'input.jpg')
        self.currentImage = self.baseImage.copy()
        self.SetMaskLists()

    def InstanceSelect(self, index):
        print("Selected instance: " + str(index))
        self.selectedMask = self.maskList[index]
        self.selectedIsGroup = False

    def ClassSelect(self, index):
        print("Selected class: " + str(index))
        self.selectedMask = self.classList[index]
        self.selectedIsGroup = True

    def DrawCurrentImage(self):

        drawingImg = self.baseImage.copy()
        for mask in self.maskList:

            groupSettings = []
            for cMask in self.classList:
                if cMask.maskList.__contains__(mask):
                    groupSettings.append(cMask.maskSettings)

            for gMask in self.groupList:
                if gMask.maskList.__contains__(mask):
                    groupSettings.append(gMask.maskSettings)

            totalBrightness = mask.maskSettings.brightness
            totalSaturation = mask.maskSettings.saturation

            for settings in groupSettings:
                totalBrightness += settings.brightness
                totalSaturation += settings.saturation

            drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
            drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

            drawingImg = np.where(self.selectedMask.maskTrueFalse == True, drawingImg, self.currentImage)

        cv2.imwrite(self.imagePath + 'p6_maskedit.png', drawingImg)
        pixmap = QPixmap(self.imagePath + 'p6_maskedit.png')
        self.displayGraphic.setPixmap(pixmap)
        self.currentImage = drawingImg

    # By only operating on the bounding box of the mask, this version gains a little speed
    def DrawMask(self, mask):
        drawingImg = self.baseImage.copy()[mask.minX:mask.maxX, mask.minY:mask.maxY]

        groupSettings = []
        for cMask in self.classList:
            if cMask.maskList.__contains__(mask):
                groupSettings.append(cMask.maskSettings)

        for gMask in self.groupList:
            if gMask.maskList.__contains__(mask):
                groupSettings.append(gMask.maskSettings)

        totalBrightness = mask.maskSettings.brightness
        totalSaturation = mask.maskSettings.saturation

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation

        drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
        drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

        blankImg = self.baseImage.copy()
        blankImg[mask.minX:mask.maxX, mask.minY:mask.maxY] = drawingImg
        mergedImg = np.where(mask.maskTrueFalse == True, blankImg, self.currentImage)

        cv2.imwrite(self.imagePath + 'p6_maskedit.png', mergedImg)
        pixmap = QPixmap(self.imagePath + 'p6_maskedit.png')
        self.displayGraphic.setPixmap(pixmap)
        self.currentImage = mergedImg

    # This version is slightly slower than the new one
    def DrawMaskOLD(self, mask):
        drawingImg = self.baseImage.copy()

        groupSettings = []
        for cMask in self.classList:
            if cMask.maskList.__contains__(mask):
                groupSettings.append(cMask.maskSettings)

        for gMask in self.groupList:
            if gMask.maskList.__contains__(mask):
                groupSettings.append(gMask.maskSettings)

        totalBrightness = mask.maskSettings.brightness
        totalSaturation = mask.maskSettings.saturation

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation

        drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
        drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

        mergedImg = np.where(mask.maskTrueFalse == True, drawingImg, self.currentImage)

        cv2.imwrite('imageData/p6_maskedit.png', mergedImg)
        pixmap = QPixmap('imageData/p6_maskedit.png')
        self.displayGraphic.setPixmap(pixmap)
        self.currentImage = mergedImg

    def DrawSelectedMask(self):
        if self.selectedIsGroup:
            for mask in self.selectedMask.maskList:
                self.DrawMask(mask)
        else:
            print("started drawing")
            self.DrawMask(self.selectedMask)
            print("completed drawing")




    def BrightnessChange(self, sliderValue):
        self.selectedMask.maskSettings.brightness = sliderValue
        if timeit.default_timer() - self.drawTimer > .1:
            self.DrawSelectedMask()
            self.drawTimer = timeit.default_timer()
    def BrightnessChangeForce(self):
        self.DrawSelectedMask()
    def getCurrentBrightness(self):
        return self.selectedMask.maskSettings.brightness

    def SaturationChange(self, sliderValue):
        self.selectedMask.maskSettings.saturation = sliderValue
        if timeit.default_timer() - self.drawTimer > .1:
            self.DrawSelectedMask()
            self.drawTimer = timeit.default_timer()
    def SaturationChangeForce(self):
        self.DrawSelectedMask()
    def getCurrentSaturation(self):
        return self.selectedMask.maskSettings.saturation

    def UpdateCurveTool(self, value1, value2, value3):
        print("update curvetool")

    def BlurChange(self, blurValue, backgroundState, filterState):
        self.blur.BlurFilter(self.currentImage, self.selectedMask, self.imagePath, blurValue, backgroundState, filterState)
        self.displayGraphic.setPixmap(QPixmap(self.imagePath + 'p6_maskedit.png'))
