import cv2
import numpy as np
import timeit
import random
from PyQt5.QtGui import QPixmap

from LoadedImage import LoadedImage
from MaskSelection import MaskSelection
from SimpleEdits import SimpleEdits
from CurveTool import CurveTool
from Blur import Blur


class MaskManager:

    def __init__(self):
        print("MaskManager made")

        self.imageBasePath = 'imageData/'
        self.inputFilename = '/input.jpg'
        self.editFilename = '/p6_mask_edit.png'
        self.blurFilename = '/p6_blur_edit.png'
        self.outlineFilename = '/p6_outline_edit.png'

        self.baseGraphic = None

        self.displayGraphicLabel = None
        self.instanceDropdown = None
        self.classDropdown = None
        self.groupDropdown = None

        self.simpleEdits = SimpleEdits()
        self.curveTool = CurveTool()
        self.blur = Blur()

        self.loadedImages = []
        self.selectedMask = None
        self.selectedImage = None
        self.selectedIsGroup = False

        self.showOutline = False
        self.drawTimer = timeit.default_timer()

    def SetUIreferences(self, imageLabel, instanceDropdown, classDropDown):
        self.displayGraphicLabel = imageLabel
        self.instanceDropdown = instanceDropdown
        self.classDropdown = classDropDown

    def SetMaskLists(self):

        self.instanceDropdown.clear()
        for mask in self.selectedImage.maskList:
            self.instanceDropdown.addItem(mask.maskName)

        self.classDropdown.clear()
        for maskClass in self.selectedImage.classList:
            self.classDropdown.addItem(maskClass.groupName)

        self.selectedMask = self.selectedImage.maskList[0]

    def GetImageMasks(self, loadedImage):
        loadedImage.maskList, loadedImage.classList = MaskSelection().DetectMasks(self.imageFullPath)

    def ImageSelect(self, imageName):
        print("Switched to image: " + imageName)
        self.imageFullPath = self.imageBasePath + imageName + "/"
        self.displayGraphicLabel.setPixmap(QPixmap(self.imageFullPath + self.inputFilename))
        self.baseGraphic = cv2.imread(self.imageFullPath + self.inputFilename)

        newImage = None
        for image in self.loadedImages:
            print(image.imageName + " --- " + imageName)
            if image.imageName == imageName:
                newImage = image
                break

        if newImage is None:
            newImage = self.CreateMaskImage(imageName)

        self.selectedImage = newImage
        self.displayGraphicLabel.setPixmap(QPixmap(self.imageFullPath + self.editFilename))
        self.SetMaskLists()

    def CreateMaskImage(self, imageName):
        newImage = LoadedImage()
        newImage.imageName = imageName
        newImage.baseImagePath = self.imageBasePath + imageName + self.inputFilename
        newImage.editImagePath = self.imageBasePath + imageName + self.editFilename
        newImage.baseGraphic = cv2.imread(self.imageBasePath + imageName + self.inputFilename)
        newImage.currentGraphic = newImage.baseGraphic.copy()
        cv2.imwrite(newImage.editImagePath, newImage.currentGraphic)

        self.loadedImages.append(newImage)
        self.GetImageMasks(newImage)

        return newImage

    def InstanceSelect(self, index):
        print("Selected instance: " + str(index))
        self.selectedMask = self.selectedImage.maskList[index]
        self.selectedIsGroup = False
        if self.showOutline is True:
            self.ShowOutline()

    def ClassSelect(self, index):
        print("Selected class: " + str(index))
        self.selectedMask = self.selectedImage.classList[index]
        self.selectedIsGroup = True
        if self.showOutline is True:
            self.ShowOutline()

    def ReDrawCurrentImage(self):
        pixmap = QPixmap(self.imageFullPath + self.editFilename)
        self.displayGraphicLabel.setPixmap(pixmap)
        if self.showOutline is True:
            self.ShowOutline()

    def DrawCurrentImage(self):
        drawingImg = self.baseGraphic.copy()
        for mask in self.selectedImage.maskList:

            groupSettings = []
            for cMask in self.selectedImage.classList:
                if cMask.maskList.__contains__(mask):
                    groupSettings.append(cMask.maskSettings)

            for gMask in self.selectedImage.groupList:
                if gMask.maskList.__contains__(mask):
                    groupSettings.append(gMask.maskSettings)

            totalBrightness = mask.maskSettings.brightness
            totalSaturation = mask.maskSettings.saturation

            for settings in groupSettings:
                totalBrightness += settings.brightness
                totalSaturation += settings.saturation

            drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
            drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

            drawingImg = np.where(self.selectedMask.maskTrueFalse == True, drawingImg, self.selectedImage.currentGraphic)

        cv2.imwrite(self.imageFullPath + self.editFilename, drawingImg)
        pixmap = QPixmap(self.imageFullPath + self.editFilename)
        self.displayGraphicLabel.setPixmap(pixmap)
        self.selectedImage.currentGraphic = drawingImg

    # By only operating on the bounding box of the mask, this version gains a little speed
    def DrawMask(self, mask):
        drawingImg = self.baseGraphic.copy()[mask.minX:mask.maxX, mask.minY:mask.maxY]

        groupSettings = []
        for cMask in self.selectedImage.classList:
            if cMask.maskList.__contains__(mask):
                groupSettings.append(cMask.maskSettings)

        for gMask in self.selectedImage.groupList:
            if gMask.maskList.__contains__(mask):
                groupSettings.append(gMask.maskSettings)

        totalBrightness = mask.maskSettings.brightness
        totalSaturation = mask.maskSettings.saturation

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation

        drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
        drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

        blankImg = self.baseGraphic.copy()
        blankImg[mask.minX:mask.maxX, mask.minY:mask.maxY] = drawingImg
        mergedImg = np.where(mask.maskTrueFalse == True, blankImg, self.selectedImage.currentGraphic)

        cv2.imwrite(self.imageFullPath + self.editFilename, mergedImg)
        pixmap = QPixmap(self.imageFullPath + self.editFilename)
        self.displayGraphicLabel.setPixmap(pixmap)
        self.selectedImage.currentGraphic = mergedImg

    def DrawMaskWithCurveTool(self, mask):
        drawingImg = cv2.imread("imageData/" + self.selectedImage.imageName + "/curve.png")[mask.minX:mask.maxX,
                     mask.minY:mask.maxY]
        if not drawingImg.any():
            drawingImg = self.baseGraphic.copy()[mask.minX:mask.maxX, mask.minY:mask.maxY]

        groupSettings = []
        for cMask in self.selectedImage.classList:
            if cMask.maskList.__contains__(mask):
                groupSettings.append(cMask.maskSettings)

        for gMask in self.selectedImage.groupList:
            if gMask.maskList.__contains__(mask):
                groupSettings.append(gMask.maskSettings)

        totalBrightness = mask.maskSettings.brightness
        totalSaturation = mask.maskSettings.saturation

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation

        drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
        drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

        blankImg = self.baseGraphic.copy()
        blankImg[mask.minX:mask.maxX, mask.minY:mask.maxY] = drawingImg
        mergedImg = np.where(mask.maskTrueFalse == True, blankImg, self.selectedImage.currentGraphic)

        cv2.imwrite(self.imageFullPath + self.editFilename, mergedImg)
        pixmap = QPixmap(self.imageFullPath + self.editFilename)
        self.displayGraphicLabel.setPixmap(pixmap)
        self.selectedImage.currentGraphic = mergedImg

    def DrawSelectedMask(self):
        if self.selectedIsGroup:
            for mask in self.selectedMask.maskList:
                self.DrawMask(mask)
        else:
            print("started drawing")
            self.DrawMask(self.selectedMask)
            print("completed drawing")

        self.ShowOutline()

    def ShowOutline(self):
        outlines = np.ones(self.selectedImage.currentGraphic.shape, dtype=np.uint8)
        kernel = np.ones((3, 3), np.uint8)

        for mask in self.selectedMask.getMasks():
            converted = mask.maskBlackWhite.astype(np.uint8)
            contours = cv2.findContours(converted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(outlines, contours[0], -1, (36, 255, 12), thickness=5)

        outlines = np.where(outlines > 1, outlines, self.selectedImage.currentGraphic)
        cv2.imwrite(self.imageFullPath + self.outlineFilename, outlines)
        outlinePixmap = QPixmap(self.imageFullPath + self.outlineFilename)
        self.displayGraphicLabel.setPixmap(outlinePixmap)

    def ShowOutlineNo(self):
        outline = 0
        kernel = np.ones((3, 3), np.uint8)
        for k in self.selectedMask.getMasks():
            kimg = k.maskBlackWhite.astype('uint8')
            outlines = cv2.morphologyEx(kimg, cv2.MORPH_GRADIENT, kernel)
            outlines = np.where(outlines >= 1,
                                (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)), 0)
            outline += outlines
        outline = np.where(outline >= 1, outline, self.cvimage).astype(np.uint8)
        cv2.imshow('outline', outline)

    def ShowOutlineToggle(self, toggle):
        self.showOutline = not self.showOutline
        self.ReDrawCurrentImage()
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

    def UpdateCurveTool(self, value1, value2, value3, colorChannel):
        self.curveTool.sliderChange(value1, value2, value3, colorChannel,
                                    self.selectedMask, self.selectedImage)

    def BlurChange(self, blurValue, backgroundState, filterState):
        blurImage = self.blur.BlurFilter(self.selectedImage.currentGraphic, self.selectedMask,
                                         self.imageFullPath, blurValue, backgroundState, filterState)

        if blurImage is not None:
            cv2.imwrite(self.imageFullPath + self.blurFilename, blurImage)
            self.displayGraphicLabel.setPixmap(QPixmap(self.imageFullPath + self.blurFilename))
