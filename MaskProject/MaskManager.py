import cv2
import numpy as np
import timeit
from PyQt5.QtGui import QPixmap

from MaskGroup import MaskGroup
from LoadedImage import LoadedImage
from MaskDetector import MaskSelection
from SimpleEdits import SimpleEdits
from CurveTool import CurveTool
from ToneCurve import ToneCurve
from Blur import Blur


class MaskManager:

    def __init__(self):
        #print("MaskManager made")
        self.imageBasePath = 'imageData/'
        self.imageFullPath = ""
        self.inputFilename = '/input.jpg'
        self.editFilename = '/p6_mask_edit.png'
        self.blurFilename = '/p6_blur_edit.png'
        self.outlineFilename = '/p6_outline_edit.png'

        self.baseGraphic = None
        self.displayGraphicLabel = None
        self.currentSelectionText = None

        self.instanceDropdown = None
        self.classDropdown = None
        self.groupDropdown = None
        self.newGroupMaskWindow = None
        self.deleteDropdown = None

        self.simpleEdits = SimpleEdits()
        self.curveTool = CurveTool()
        self.toneCurve = ToneCurve()
        self.blur = Blur()

        self.loadedImages = []
        self.selectedMask = None
        self.selectedImage = None

        self.showOutline = True
        self.drawTimer = timeit.default_timer()

    def SetUIreferences(self, imageLabel, currentSelectionText,
                        instanceDropdown, classDropDown, groupDropdown, maskWindow, deleteDropdown):
        self.displayGraphicLabel = imageLabel
        self.currentSelectionText = currentSelectionText
        self.instanceDropdown = instanceDropdown
        self.classDropdown = classDropDown
        self.groupDropdown = groupDropdown
        self.newGroupMaskWindow = maskWindow
        self.deleteDropdown = deleteDropdown

    def SetMaskLists(self):
        self.instanceDropdown.clear()
        self.newGroupMaskWindow.clear()
        for mask in self.selectedImage.maskList:
            self.instanceDropdown.addItem(mask.maskName)
            self.newGroupMaskWindow.addItem(mask.maskName)

        self.classDropdown.clear()
        for maskClass in self.selectedImage.classList:
            self.classDropdown.addItem(maskClass.maskName)

        self.groupDropdown.clear()
        self.deleteDropdown.clear()
        for maskGroup in self.selectedImage.groupList:
            self.groupDropdown.addItem(maskGroup.maskName)
            self.deleteDropdown.addItem(maskGroup.maskName)

        self.SetSelectedMask(self.selectedImage.maskList[0], "Mask")

    def SetSelectedMask(self, mask, typeText):
        self.selectedMask = mask
        self.currentSelectionText.setText("Current mask selection: " + typeText + "_" + mask.maskName)

    def GetImageMasks(self, loadedImage):
        loadedImage.maskList, loadedImage.classList = MaskSelection().DetectMasks(self.imageFullPath)

    def ImageSelect(self, imageName):
        #print("Switched to image: " + imageName)
        self.imageFullPath = self.imageBasePath + imageName + "/"
        self.displayGraphicLabel.setPixmap(QPixmap(self.imageFullPath + self.inputFilename))
        self.baseGraphic = cv2.imread(self.imageFullPath + self.inputFilename)

        newImage = None
        for image in self.loadedImages:
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

    def DisplayCurrentImage(self):
        pixmap = QPixmap(self.imageFullPath + self.editFilename)
        self.displayGraphicLabel.setPixmap(pixmap)

        if self.showOutline is True:
            self.ShowOutline()

    def DisplayBaseImage(self):
        pixmap = QPixmap(self.imageFullPath + self.inputFilename)
        self.displayGraphicLabel.setPixmap(pixmap)

        self.newGroupMaskWindow.clearSelection()

    #Completely redraws the image from the ground up, actually completely unused?
    def RedrawCurrentImage(self):
        drawingImg = self.baseGraphic.copy()

        for mask in self.selectedImage.maskList:
            perMaskImg = self.baseGraphic.copy()
            groupSettings = []
            for cMask in self.selectedImage.classList:
                if cMask.maskList.__contains__(mask):
                    groupSettings.append(cMask.maskSettings)

            for gMask in self.selectedImage.groupList:
                if gMask.maskList.__contains__(mask):
                    groupSettings.append(gMask.maskSettings)

            totalBrightness = mask.maskSettings.brightness
            totalSaturation = mask.maskSettings.saturation
            totalColor1 = mask.maskSettings.colorCurve1
            totalColor2 = mask.maskSettings.colorCurve2
            totalColor3 = mask.maskSettings.colorCurve3
            channel = mask.maskSettings.colorChannel

            for settings in groupSettings:
                totalBrightness += settings.brightness
                totalSaturation += settings.saturation
                totalColor1 += settings.colorCurve1
                totalColor2 += settings.colorCurve2
                totalColor3 += settings.colorCurve3

            if totalColor1 != 0 or totalColor2 != 0 or totalColor3 != 0:
                drawingImg = self.curveTool.ApplyColorCurve(totalColor1, totalColor2, totalColor3, channel, drawingImg)
            if totalBrightness != 0:
                perMaskImg = self.simpleEdits.DrawBrightness(totalBrightness, perMaskImg)
            if totalSaturation != 0:
                perMaskImg = self.simpleEdits.DrawSaturation(totalSaturation, perMaskImg)

            drawingImg = np.where(mask.maskTrueFalse == True, perMaskImg, drawingImg)

        cv2.imwrite(self.imageFullPath + self.editFilename, drawingImg)
        self.selectedImage.currentGraphic = drawingImg

        if self.showOutline is True:
            self.ShowOutline()

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
        totalColor1 = mask.maskSettings.colorCurve1
        totalColor2 = mask.maskSettings.colorCurve2
        totalColor3 = mask.maskSettings.colorCurve3
        channel = mask.maskSettings.colorChannel

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation
            totalColor1 += settings.colorCurve1
            totalColor2 += settings.colorCurve2
            totalColor3 += settings.colorCurve3

        if totalColor1 != 0 or totalColor2 != 0 or totalColor3 != 0:
            drawingImg = self.curveTool.ApplyColorCurve(totalColor1, totalColor2, totalColor3, channel, drawingImg)
        if totalBrightness != 0:
            drawingImg = self.simpleEdits.DrawBrightness(totalBrightness, drawingImg)
        if totalSaturation != 0:
            drawingImg = self.simpleEdits.DrawSaturation(totalSaturation, drawingImg)

        blankImg = self.baseGraphic.copy()
        blankImg[mask.minX:mask.maxX, mask.minY:mask.maxY] = drawingImg
        mergedImg = np.where(mask.maskTrueFalse == True, blankImg, self.selectedImage.currentGraphic)

        cv2.imwrite(self.imageFullPath + self.editFilename, mergedImg)
        self.selectedImage.currentGraphic = mergedImg

    def DrawSelectedMask(self):
        if timeit.default_timer() - self.drawTimer > .1:
            self.drawTimer = timeit.default_timer()

            for mask in self.selectedMask.GetMasks():
                self.DrawMask(mask)

            self.DisplayCurrentImage()

    def ShowOutline(self):
        outlines = np.ones(self.selectedImage.currentGraphic.shape, dtype=np.uint8)

        for mask in self.selectedMask.GetMasks():
            converted = mask.maskBlackWhite.astype(np.uint8)
            contours = cv2.findContours(converted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(outlines, contours[0], -1, (36, 255, 12), thickness=2)

        outlines = np.where(outlines > 1, outlines, self.selectedImage.currentGraphic)
        cv2.imwrite(self.imageFullPath + self.outlineFilename, outlines)
        outlinePixmap = QPixmap(self.imageFullPath + self.outlineFilename)
        self.displayGraphicLabel.setPixmap(outlinePixmap)

    def ShowOutlineToggle(self):
        print("Toggle show outline")
        self.showOutline = not self.showOutline
        self.DisplayCurrentImage()

    def ShowCreateOutlines(self):
        outlines = np.ones(self.selectedImage.currentGraphic.shape, dtype=np.uint8)

        outLineMasks = []
        for name in self.newGroupMaskWindow.selectedItems():
            for mask in self.selectedImage.maskList:
                if name.text() == mask.maskName:
                    outLineMasks.append(mask)

        for mask in outLineMasks:
            converted = mask.maskBlackWhite.astype(np.uint8)
            contours = cv2.findContours(converted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(outlines, contours[0], -1, (36, 255, 12), thickness=2)

        outlines = np.where(outlines > 1, outlines, self.selectedImage.baseGraphic)
        cv2.imwrite(self.imageFullPath + self.outlineFilename, outlines)
        outlinePixmap = QPixmap(self.imageFullPath + self.outlineFilename)
        self.displayGraphicLabel.setPixmap(outlinePixmap)

    def InstanceSelect(self, index):
        #print("Selected instance: " + str(index))
        self.SetSelectedMask(self.selectedImage.maskList[index], "Mask")
        if self.showOutline is True:
            self.ShowOutline()

    def ClassSelect(self, index):
        #print("Selected class: " + str(index))
        self.SetSelectedMask(self.selectedImage.classList[index], "Class")
        if self.showOutline is True:
            self.ShowOutline()
    def GroupSelect(self, index):
        #print("Selected group: " + str(index))
        self.SetSelectedMask(self.selectedImage.groupList[index], "Group")
        if self.showOutline is True:
            self.ShowOutline()

    def CreateGroup(self, newName):
        if newName == "":
            print("Cannot create group without a name")
            return
        for group in self.selectedImage.groupList:
            if group.maskName == newName:
                print("Cannot create multiple groups with the same name")
                return

        newGroup = MaskGroup(newName)
        for item in self.newGroupMaskWindow.selectedItems():
            for mask in self.selectedImage.maskList:
                if item.text() == mask.maskName:
                    newGroup.AddMask(mask)
        self.groupDropdown.addItem(newGroup.maskName)
        self.deleteDropdown.addItem(newGroup.maskName)
        self.selectedImage.groupList.append(newGroup)
        self.selectedMask = newGroup

    def RemoveGroup(self, groupName):
        for group in self.selectedImage.groupList:
            if group.maskName == groupName:
                self.selectedImage.groupList.remove(group)
        index = self.deleteDropdown.findText(groupName)
        self.deleteDropdown.removeItem(index)
        index = self.groupDropdown.findText(groupName)
        self.groupDropdown.removeItem(index)

        if self.selectedMask.maskName == groupName:
            self.selectedMask = self.selectedImage.maskList[0]

        self.RedrawCurrentImage()

    def BrightnessChange(self, sliderValue):
        self.selectedMask.maskSettings.brightness = sliderValue
        self.DrawSelectedMask()
    def BrightnessChangeForce(self):
        self.DrawSelectedMask()
    def getCurrentBrightness(self):
        return self.selectedMask.maskSettings.brightness

    def SaturationChange(self, sliderValue):
        self.selectedMask.maskSettings.saturation = sliderValue
        self.DrawSelectedMask()
    def SaturationChangeForce(self):
        self.DrawSelectedMask()
    def getCurrentSaturation(self):
        return self.selectedMask.maskSettings.saturation

    def UpdateCurveTool(self, value1, value2, value3, colorChannel):
        #self.curveTool.ApplyColorCurve(value1, value2, value3, colorChannel, self.selectedImage)
        self.selectedMask.SetColorValues(value1, value2, value3, colorChannel)
        self.DrawSelectedMask()
    def getCurrentColorValues(self):
        value1 = self.selectedMask.maskSettings.colorCurve1
        value2 = self.selectedMask.maskSettings.colorCurve2
        value3 = self.selectedMask.maskSettings.colorCurve3
        channel = self.selectedMask.maskSettings.colorChannel
        return value1, value2, value3, channel

    def DrawHistogram(self, dropdownSelection):
        print(dropdownSelection)
        self.toneCurve.DrawHistogram(dropdownSelection, self.selectedImage.currentGraphic)

    def ToneCurveApply(self, dropdownSelection):
        self.toneCurve.ApplyFilter(dropdownSelection, self.selectedImage.currentGraphic)



    def BlurChange(self, blurValue, backgroundState, filterState):
        blurImage = self.blur.BlurFilter(self.selectedImage.currentGraphic, self.selectedMask,
                                         self.imageFullPath, blurValue, backgroundState, filterState)
        if blurImage is not None:
            cv2.imwrite(self.imageFullPath + self.blurFilename, blurImage)
            self.displayGraphicLabel.setPixmap(QPixmap(self.imageFullPath + self.blurFilename))
