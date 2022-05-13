import sys
import numpy as np
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSlider, QTabWidget, QComboBox, QLineEdit, \
    QPushButton, QCheckBox, QFileDialog, QApplication

import cv2
from MaskManager import MaskManager
#from pyQT.maskSelection import MaskSelection
#from pyQT.kernel import Kernel
#from pyQT.curveTool import curveTool
#from pyQT.BrightnessSaturation import BrightnessSaturation

class MaskUI:

#def load_image(self):
    #   path, _ = QFileDialog.getOpenFileName(None, "Load Image", "")
    # if path:
    #      self.load_file(path)
    #    self.pixmap =
    def save(self):
        cv2.imwrite("save.png", self.cvimage)

    #def showOutline(self):
     ##  kernel = np.ones((3, 3), np.uint8)
      #  print(len(self.maskManager.maskList))
      #  for i in self.maskManager.maskList:
      #      conv = i.maskImage.astype(np.uint8)
      #      outlines = cv2.morphologyEx(conv, cv2.MORPH_GRADIENT, kernel)
      #      outlines = np.where(outlines >= 1, 255, 0)
      #      outline += outlines
      #  outline = np.where(outline >= 1, outlines, np.tile(self.cvimage,(1,4))).astype(np.uint8)
      #  cv2.imshow('outline', outline)

    def TabSwitch(self, index):
        if index == 0:
            print("Switched to Mask Selection tab")
        if index == 1:
            print("Switched to Saturation/Brightness tab")
            self.sliderBrightness.setSliderPosition(self.maskManager.getCurrentBrightness())
            self.sliderSaturation.setSliderPosition(self.maskManager.getCurrentSaturation())
        if index == 2:
            print("Switched to CurveTool tab")
        if index == 3:
            print("Switched to Blur Filter tab")

    def updateButton(self):
        self.mathpixmap = QPixmap('plot.png')
        #self.labelmathpixmap.setPixmap(self.mathpixmap)
        self.window.update()

    def updateWindow(self):
        print("updating window")
        #self.pixmap = QPixmap('edit.png')
        print("set to imagelabels")
        for i in self.imageLabel:
            i.setPixmap(self.pixmap)
        print("success")
        #self.current_edit = cv2.imread("edit.png")
        #self.cvimageNoBlur = cv2.imread('noBlur.png')
        self.window.update()
        print("updated window")

    def UpdateCurveToolWindow(self):
        print("update CurveTool Window")

    def UpdateCurve(self):
        print("update curve")

    def BuildUI(self):
        app = QApplication(sys.argv)

        window = QWidget()
        mainImage = QLabel()
        mainPixmap = QPixmap('images/img.jpg')
        mainImage.setPixmap(mainPixmap)
        self.maskManager = MaskManager(mainImage)

        maskSelectLayout = QVBoxLayout()
        simpleEditLayout = QVBoxLayout()
        curveToolLayout = QVBoxLayout()
        blurLayout = QVBoxLayout()

        tabWindow = QTabWidget()
        tabWindow.currentChanged.connect(self.TabSwitch)


        #TAB 1 - MASK SELECTION
        tabMaskSelect = QWidget()

        labelInstance = QLabel("Instance Selection")
        dropdownInstances = QComboBox()
        for mask in self.maskManager.maskList:
            dropdownInstances.addItem(mask.maskName)
        dropdownInstances.activated.connect(self.maskManager.InstanceSelect)

        labelClasses = QLabel("Classes")
        dropdownClasses = QComboBox()
        for mask in self.maskManager.classList:
            dropdownClasses.addItem(mask.groupName)
        dropdownClasses.activated.connect(self.maskManager.ClassSelect)

        maskSelectLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        maskSelectLayout.addWidget(labelInstance)
        maskSelectLayout.addWidget(dropdownInstances)
        maskSelectLayout.addWidget(labelClasses)
        maskSelectLayout.addWidget(dropdownClasses)


        #TAB 2 - SIMPLE EDITS
        tabSimpleEdit = QWidget()

        labelBrightness = QLabel("Brightness")
        self.sliderBrightness = QSlider(Qt.Orientation.Horizontal)
        self.sliderBrightness.setMinimum(-255)
        self.sliderBrightness.setMaximum(255)
        self.sliderBrightness.setSliderPosition(0)
        labelBrightSlider = QLabel(str(self.sliderBrightness.value()))
        self.sliderBrightness.valueChanged.connect(self.maskManager.BrightnessChange)
        self.sliderBrightness.sliderReleased.connect(self.maskManager.BrightnessChangeForce)
        self.sliderBrightness.valueChanged.connect(lambda: labelBrightSlider.setText(str(self.sliderBrightness.value())))
        layoutBrightness = QHBoxLayout()
        layoutBrightness.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layoutBrightness.addWidget(labelBrightness)
        layoutBrightness.addWidget(labelBrightSlider)

        labelSaturation = QLabel("Saturation")
        self.sliderSaturation = QSlider(Qt.Orientation.Horizontal)
        self.sliderSaturation.setMinimum(-255)
        self.sliderSaturation.setMaximum(255)
        self.sliderSaturation.setSliderPosition(0)
        labelSatSlider = QLabel(str(self.sliderSaturation.value()))
        self.sliderSaturation.valueChanged.connect(self.maskManager.SaturationChange)
        self.sliderSaturation.sliderReleased.connect(self.maskManager.SaturationChangeForce)
        self.sliderSaturation.valueChanged.connect(lambda: labelSatSlider.setText(str(self.sliderSaturation.value())))
        layoutSaturation = QHBoxLayout()
        layoutSaturation.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layoutSaturation.addWidget(labelSaturation)
        layoutSaturation.addWidget(labelSatSlider)

        simpleEditLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        simpleEditLayout.addLayout(layoutBrightness)
        simpleEditLayout.addWidget(self.sliderBrightness)
        simpleEditLayout.addLayout(layoutSaturation)
        simpleEditLayout.addWidget(labelSatSlider)
        simpleEditLayout.addWidget(self.sliderSaturation)



        #TAB 3 - CURVE TOOL
        tabCurveTool = QWidget()

        lineEditLabel1 = QLabel("Value 1")
        lineEditValue1 = QLineEdit()
        lineEditLayout1 = QHBoxLayout()
        lineEditLayout1.addWidget(lineEditLabel1)
        lineEditLayout1.addWidget(lineEditValue1)

        lineEditLabel2 = QLabel("Value 2")
        lineEditValue2 = QLineEdit()
        lineEditLayout2 = QHBoxLayout()
        lineEditLayout2.addWidget(lineEditLabel2)
        lineEditLayout2.addWidget(lineEditValue2)

        lineEditLabel3 = QLabel("Value 3")
        lineEditValue3 = QLineEdit()
        lineEditLayout3 = QHBoxLayout()
        lineEditLayout3.addWidget(lineEditLabel3)
        lineEditLayout3.addWidget(lineEditValue3)

        lineEditValue1.editingFinished.connect(lambda: self.maskManager.UpdateCurveTool(lineEditValue1.text(), lineEditValue2.text(), lineEditValue3.text()))
        lineEditValue2.editingFinished.connect(lambda: self.maskManager.UpdateCurveTool(lineEditValue1.text(), lineEditValue2.text(), lineEditValue3.text()))
        lineEditValue3.editingFinished.connect(lambda: self.maskManager.UpdateCurveTool(lineEditValue1.text(), lineEditValue2.text(), lineEditValue3.text()))
        lineEditValue1.editingFinished.connect(self.UpdateCurveToolWindow)
        lineEditValue2.editingFinished.connect(self.UpdateCurveToolWindow)
        lineEditValue3.editingFinished.connect(self.UpdateCurveToolWindow)

        curveToolImage = QLabel()
        curveToolPixmap = QPixmap('images/plot.png')
        curveToolImage.setPixmap(curveToolPixmap)

        curveUpdateBtn = QPushButton("Update Curve")
        curveUpdateBtn.clicked.connect(self.UpdateCurve)

        colorChannelSelect = QComboBox()
        colorChannelSelect.addItems(["Red", "Green", "Blue"])

        curveToolLayout.addLayout(lineEditLayout1)
        curveToolLayout.addLayout(lineEditLayout2)
        curveToolLayout.addLayout(lineEditLayout3)
        curveToolLayout.addWidget(curveToolImage)
        curveToolLayout.addWidget(curveUpdateBtn)
        curveToolLayout.addWidget(colorChannelSelect)


        #TAB 4 - BLUR FILTER
        tabBlur = QWidget()

        applyBackgroundLabel = QLabel("Apply to Background")
        applyBackgroundCheck = QCheckBox()
        applyBackgroundLayout = QHBoxLayout()
        applyBackgroundLayout.addWidget(applyBackgroundLabel)
        applyBackgroundLayout.addWidget(applyBackgroundCheck)
        applyBackgroundLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        applyBackgroundCheck.stateChanged.connect(self.maskManager.ToggleBlurBackground)

        applyFilterLabel = QLabel("Apply Filter")
        applyFilterCheck = QCheckBox()
        applyFilterLayout = QHBoxLayout()
        applyFilterLayout.addWidget(applyFilterLabel)
        applyFilterLayout.addWidget(applyFilterCheck)
        applyFilterLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        applyFilterCheck.stateChanged.connect(self.maskManager.ToggleBlurFilter)

        blurIntensityLabel = QLabel("Blur Intensity")
        blurIntensitySlider = QSlider(Qt.Orientation.Horizontal)
        blurIntensitySlider.setMinimum(1)
        blurIntensitySlider.setMaximum(10)
        blurIntensitySlider.valueChanged.connect(lambda: self.maskManager.BlurChange(blurIntensitySlider.value(), applyBackgroundCheck.checkState(), applyFilterCheck.checkState()))

        blurLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        blurLayout.addLayout(applyBackgroundLayout)
        blurLayout.addLayout(applyFilterLayout)
        blurLayout.addWidget(blurIntensityLabel)
        blurLayout.addWidget(blurIntensitySlider)


        #SET LAYOUT
        mainLayout = QHBoxLayout()

        tabMaskSelect.setLayout(maskSelectLayout)
        tabSimpleEdit.setLayout(simpleEditLayout)
        tabCurveTool.setLayout(curveToolLayout)
        tabBlur.setLayout(blurLayout)

        tabWindow.addTab(tabMaskSelect, "Mask")
        tabWindow.addTab(tabSimpleEdit, "Adjustments")
        tabWindow.addTab(tabCurveTool, "Curve Tool")
        tabWindow.addTab(tabBlur, "Blur")

        mainLayout.addWidget(mainImage)
        mainLayout.addWidget(tabWindow)


        window.setWindowTitle("Mask Manager")
        window.setGeometry(100, 100, 800, 500)
        window.setLayout(mainLayout)
        window.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        window.show()
        window.setFixedSize(window.size())
        sys.exit(app.exec_())

if __name__ == '__main__':
    ui = MaskUI()
    ui.BuildUI()