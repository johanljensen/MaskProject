import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSlider, QTabWidget, QComboBox, QLineEdit, \
    QPushButton, QCheckBox, QApplication, QListWidget, QAbstractItemView

from MaskManager import MaskManager

class MaskUI:

    def TabSwitch(self, index):
        self.maskManager.DisplayCurrentImage()

        if index == 0:
            #print("Switched to Mask Selection tab")
            if not self.maskSelectPage.isVisible():
                self.maskSelectPage.show()
                self.createGroupPage.hide()

        if index == 1:
            #print("Switched to Saturation/Brightness tab")
            self.sliderBrightness.setSliderPosition(self.maskManager.getCurrentBrightness())
            self.sliderSaturation.setSliderPosition(self.maskManager.getCurrentSaturation())
        if index == 2:
            #print("Switched to CurveTool tab")
            value1, value2, value3, channel = self.maskManager.getCurrentColorValues()
            self.lineEditSlider1.setSliderPosition(value1)
            self.lineEditSlider2.setSliderPosition(value2)
            self.lineEditSlider3.setSliderPosition(value3)
            self.colorChannelSelect.setCurrentText(channel)
        #if index == 3:
            #print("Switched to Tone Curve tab")
        #if index == 4:
            #print("Switched to Blur Filter tab")

    def ToggleMaskSelectGroupCreate(self):
        if self.maskSelectPage.isVisible():
            self.maskSelectPage.setVisible(False)
            self.createGroupPage.setVisible(True)
            self.maskManager.DisplayBaseImage()
        else:
            self.maskSelectPage.setVisible(True)
            self.createGroupPage.setVisible(False)
            self.maskManager.DisplayCurrentImage()

    def UpdateCurveToolWindow(self):
        curveToolPixmap = QPixmap('imageData/curveToolPlot.png')
        self.curveToolImage.setPixmap(curveToolPixmap)

    def UpdateToneCurvePlot(self):
        toneCurvePixmap = QPixmap('imageData/toneCurvePlot.png')
        self.toneCurveImage.setPixmap(toneCurvePixmap)

    def BuildUI(self):
        app = QApplication(sys.argv)

        window = QWidget()
        self.maskManager = MaskManager()

        labelImageSelect = QLabel("Select image to edit")
        dropdownImages = QComboBox()
        imageFolderNames = [f.name for f in os.scandir("imageData") if f.is_dir()]
        dropdownImages.addItems(imageFolderNames)
        dropdownImages.setCurrentText("Royal Guard")

        mainImage = QLabel()

        currentSelectionLabel = QLabel()

        self.outlineToggle = QCheckBox()
        self.outlineToggle.setChecked(True)
        outlineText = QLabel("Show mask outlines")
        outlineLayout = QHBoxLayout()
        outlineLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        outlineLayout.addWidget(self.outlineToggle)
        outlineLayout.addWidget(outlineText)

        imageDisplayLayout = QVBoxLayout()
        imageDisplayLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        imageDisplayLayout.addWidget(labelImageSelect)
        imageDisplayLayout.addWidget(dropdownImages)
        imageDisplayLayout.addWidget(mainImage)
        imageDisplayLayout.addWidget(currentSelectionLabel)
        imageDisplayLayout.addLayout(outlineLayout)


        #TAB 1 - MASK SELECTION
        tabMaskSelect = QWidget()

        labelInstance = QLabel("Instance Selection")
        listviewInstances = QListWidget()
        labelClasses = QLabel("Classes")
        listviewClasses = QListWidget()
        labelGroups = QLabel("Groups")
        listviewGroups = QListWidget()

        openCreateGroupBtn = QPushButton("Create Group")

        self.maskSelectPage = QWidget()
        maskSelectLayout = QVBoxLayout()
        maskSelectLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        maskSelectLayout.addWidget(labelInstance)
        maskSelectLayout.addWidget(listviewInstances)
        maskSelectLayout.addWidget(labelClasses)
        maskSelectLayout.addWidget(listviewClasses)
        maskSelectLayout.addWidget(labelGroups)
        maskSelectLayout.addWidget(listviewGroups)
        maskSelectLayout.addWidget(openCreateGroupBtn)
        self.maskSelectPage.setLayout(maskSelectLayout)

        newGroupBtn = QPushButton("Create group with selected masks")
        newGroupName = QLineEdit("Insert name")

        maskList = QListWidget()
        maskList.setSelectionMode(QAbstractItemView.MultiSelection)
        maskList.setMaximumHeight(250)

        createBtnNameLayout = QHBoxLayout()
        createBtnNameLayout.addWidget(newGroupBtn)
        createBtnNameLayout.addWidget(newGroupName)

        deleteGroupList = QListWidget()
        deleteGroupBtn = QPushButton("Delete selected mask group")
        deleteGroupBtn.setMaximumWidth(150)
        deleteGroupBtn.setMinimumWidth(150)

        closeCreateGroupBtn = QPushButton("Return to Mask Select")

        self.createGroupPage = QWidget()
        createGroupLayout = QVBoxLayout()
        createGroupLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        createGroupLayout.addWidget(maskList)
        createGroupLayout.addLayout(createBtnNameLayout)
        createGroupLayout.addWidget(deleteGroupList)
        createGroupLayout.addWidget(deleteGroupBtn)
        createGroupLayout.addWidget(closeCreateGroupBtn)
        self.createGroupPage.setLayout(createGroupLayout)
        self.createGroupPage.setVisible(False)

        maskManagementLayout = QVBoxLayout()
        maskManagementLayout.addWidget(self.maskSelectPage)
        maskManagementLayout.addWidget(self.createGroupPage)

        #TAB 2 - SIMPLE EDITS
        tabSimpleEdit = QWidget()

        labelBrightness = QLabel("Brightness")
        self.sliderBrightness = QSlider(Qt.Orientation.Horizontal)
        self.sliderBrightness.setMinimum(-255)
        self.sliderBrightness.setMaximum(255)
        self.sliderBrightness.setSliderPosition(0)
        labelBrightSlider = QLabel(str(self.sliderBrightness.value()))

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

        layoutSaturation = QHBoxLayout()
        layoutSaturation.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layoutSaturation.addWidget(labelSaturation)
        layoutSaturation.addWidget(labelSatSlider)

        simpleEditLayout = QVBoxLayout()
        simpleEditLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        simpleEditLayout.addLayout(layoutBrightness)
        simpleEditLayout.addWidget(self.sliderBrightness)
        simpleEditLayout.addLayout(layoutSaturation)
        simpleEditLayout.addWidget(self.sliderSaturation)


        #TAB 3 - CURVE TOOL
        tabCurveTool = QWidget()

        lineEditLabel1 = QLabel("Value 1:")
        self.lineEditSlider1 = QSlider(Qt.Orientation.Horizontal)
        self.lineEditSlider1.setMinimum(-10)
        self.lineEditSlider1.setMaximum(10)
        lineEditValue1 = QLabel(str(self.lineEditSlider1.value()))
        lineEditLayout1 = QHBoxLayout()
        lineEditLayout1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lineEditLayout1.addWidget(lineEditLabel1)
        lineEditLayout1.addWidget(lineEditValue1)

        lineEditLabel2 = QLabel("Value 2:")
        self.lineEditSlider2 = QSlider(Qt.Orientation.Horizontal)
        self.lineEditSlider2.setMinimum(-10)
        self.lineEditSlider2.setMaximum(10)
        lineEditValue2 = QLabel(str(self.lineEditSlider2.value()))
        lineEditLayout2 = QHBoxLayout()
        lineEditLayout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lineEditLayout2.addWidget(lineEditLabel2)
        lineEditLayout2.addWidget(lineEditValue2)

        lineEditLabel3 = QLabel("Value 3:")
        self.lineEditSlider3 = QSlider(Qt.Orientation.Horizontal)
        self.lineEditSlider3.setMinimum(-10)
        self.lineEditSlider3.setMaximum(10)
        lineEditValue3 = QLabel(str(self.lineEditSlider3.value()))
        lineEditLayout3 = QHBoxLayout()
        lineEditLayout3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lineEditLayout3.addWidget(lineEditLabel3)
        lineEditLayout3.addWidget(lineEditValue3)

        self.colorChannelSelect = QComboBox()
        self.colorChannelSelect.addItems(["All", "Red", "Green", "Blue"])

        self.curveToolImage = QLabel()
        curveToolPixmap = QPixmap('imageData/curveToolPlot.png')
        self.curveToolImage.setPixmap(curveToolPixmap)

        curveToolLayout = QVBoxLayout()
        curveToolLayout.addLayout(lineEditLayout1)
        curveToolLayout.addWidget(self.lineEditSlider1)
        curveToolLayout.addLayout(lineEditLayout2)
        curveToolLayout.addWidget(self.lineEditSlider2)
        curveToolLayout.addLayout(lineEditLayout3)
        curveToolLayout.addWidget(self.lineEditSlider3)
        curveToolLayout.addWidget(self.colorChannelSelect)
        curveToolLayout.addWidget(self.curveToolImage)


        #TAB 4 - TONE CURVE
        tabToneCurve = QWidget()

        self.toneCurveImage = QLabel()
        toneCurvePixmap = QPixmap('imageData/toneCurvePlot.png')
        self.toneCurveImage.setPixmap(toneCurvePixmap)

        toneCurveDropdown = QComboBox()
        toneCurveDropdown.addItem("No filter")
        toneCurveDropdown.addItem("Negative reversal")
        toneCurveDropdown.addItem("Line curve")
        toneCurveDropdown.addItem("S-Curve")
        toneCurveDropdown.addItem("Solarization")
        toneCurveDropdown.addItem("Posterization")

        toneCurveButton = QPushButton("Apply to mask")

        toneCurveLayout = QVBoxLayout()
        toneCurveLayout.addWidget(self.toneCurveImage)
        toneCurveLayout.addWidget(toneCurveDropdown)
        toneCurveLayout.addWidget(toneCurveButton)


        #TAB 5 - BLUR FILTER
        tabBlur = QWidget()

        applyBackgroundLabel = QLabel("Apply to Background")
        applyBackgroundCheck = QCheckBox()
        applyBackgroundLayout = QHBoxLayout()
        applyBackgroundLayout.addWidget(applyBackgroundLabel)
        applyBackgroundLayout.addWidget(applyBackgroundCheck)
        applyBackgroundLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        applyFilterLabel = QLabel("Apply Filter")
        applyFilterCheck = QCheckBox()
        applyFilterLayout = QHBoxLayout()
        applyFilterLayout.addWidget(applyFilterLabel)
        applyFilterLayout.addWidget(applyFilterCheck)
        applyFilterLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        blurIntensityLabel = QLabel("Blur Intensity")
        blurIntensitySlider = QSlider(Qt.Orientation.Horizontal)
        blurIntensitySlider.setMinimum(1)
        blurIntensitySlider.setMaximum(10)

        blurLayout = QVBoxLayout()
        blurLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        blurLayout.addLayout(applyBackgroundLayout)
        blurLayout.addLayout(applyFilterLayout)
        blurLayout.addWidget(blurIntensityLabel)
        blurLayout.addWidget(blurIntensitySlider)


        #SET LAYOUT
        mainLayout = QHBoxLayout()

        tabMaskSelect.setLayout(maskManagementLayout)
        tabSimpleEdit.setLayout(simpleEditLayout)
        tabCurveTool.setLayout(curveToolLayout)
        tabToneCurve.setLayout(toneCurveLayout)
        tabBlur.setLayout(blurLayout)

        tabWindow = QTabWidget()
        tabWindow.addTab(tabMaskSelect, "Mask Select")
        tabWindow.addTab(tabSimpleEdit, "Adjustments")
        tabWindow.addTab(tabCurveTool, "Curve Tool")
        tabWindow.addTab(tabToneCurve, "Tone Curve")
        tabWindow.addTab(tabBlur, "Blur Filter")

        mainLayout.addLayout(imageDisplayLayout)
        mainLayout.addWidget(tabWindow)


        #SET FUNCTIONALITY
        tabWindow.currentChanged.connect(self.TabSwitch)

        self.outlineToggle.stateChanged.connect(self.maskManager.ShowOutlineToggle)

        dropdownImages.currentTextChanged.connect(self.maskManager.ImageSelect)
        dropdownImages.currentIndexChanged.connect(lambda: tabWindow.setCurrentIndex(0))
        #dropdownImages.currentIndexChanged.connect(lambda: self.outlineToggle.setChecked(False))

        #Mask select
        listviewInstances.itemClicked.connect(self.maskManager.InstanceSelect)
        listviewClasses.itemClicked.connect(self.maskManager.ClassSelect)
        listviewGroups.itemClicked.connect(self.maskManager.GroupSelect)
        openCreateGroupBtn.clicked.connect(self.ToggleMaskSelectGroupCreate)

        maskList.clicked.connect(self.maskManager.ShowCreateOutlines)
        newGroupBtn.clicked.connect(lambda:
                                    self.maskManager.CreateGroup(newGroupName.text()))
        deleteGroupList.clicked.connect(self.maskManager.ShowGroupOutlines)
        deleteGroupBtn.clicked.connect(self.maskManager.RemoveGroup)
        closeCreateGroupBtn.clicked.connect(self.ToggleMaskSelectGroupCreate)

        #Simple edits
        self.sliderBrightness.valueChanged.connect(self.maskManager.BrightnessChange)
        self.sliderBrightness.sliderReleased.connect(self.maskManager.BrightnessChangeForce)
        self.sliderBrightness.valueChanged.connect(
            lambda: labelBrightSlider.setText(str(self.sliderBrightness.value())))

        self.sliderSaturation.valueChanged.connect(self.maskManager.SaturationChange)
        self.sliderSaturation.sliderReleased.connect(self.maskManager.SaturationChangeForce)
        self.sliderSaturation.valueChanged.connect(lambda: labelSatSlider.setText(str(self.sliderSaturation.value())))

        #Color curve
        self.lineEditSlider1.valueChanged.connect(
            lambda: self.maskManager.UpdateCurveTool(self.lineEditSlider1.value(), self.lineEditSlider2.value(),
                                                     self.lineEditSlider3.value(), self.colorChannelSelect.currentText()))
        self.lineEditSlider2.valueChanged.connect(
            lambda: self.maskManager.UpdateCurveTool(self.lineEditSlider1.value(), self.lineEditSlider2.value(),
                                                     self.lineEditSlider3.value(), self.colorChannelSelect.currentText()))
        self.lineEditSlider3.valueChanged.connect(
            lambda: self.maskManager.UpdateCurveTool(self.lineEditSlider1.value(), self.lineEditSlider2.value(),
                                                     self.lineEditSlider3.value(), self.colorChannelSelect.currentText()))
        self.lineEditSlider1.valueChanged.connect(lambda: lineEditValue1.setText(str(self.lineEditSlider1.value())))
        self.lineEditSlider1.valueChanged.connect(self.UpdateCurveToolWindow)
        self.lineEditSlider2.valueChanged.connect(lambda: lineEditValue2.setText(str(self.lineEditSlider2.value())))
        self.lineEditSlider2.valueChanged.connect(self.UpdateCurveToolWindow)
        self.lineEditSlider3.valueChanged.connect(lambda: lineEditValue3.setText(str(self.lineEditSlider3.value())))
        self.lineEditSlider3.valueChanged.connect(self.UpdateCurveToolWindow)
        self.colorChannelSelect.currentIndexChanged.connect(
            lambda: self.maskManager.UpdateCurveTool(self.lineEditSlider1.value(), self.lineEditSlider2.value(),
                                                     self.lineEditSlider3.value(), self.colorChannelSelect.currentText()))

        #Tone curve
        toneCurveDropdown.currentTextChanged.connect(self.maskManager.DrawHistogram)
        toneCurveDropdown.currentTextChanged.connect(self.UpdateToneCurvePlot)

        toneCurveButton.clicked.connect(lambda: self.maskManager.ToneCurveApply(toneCurveDropdown.currentText()))

        #Blur filter
        applyBackgroundCheck.stateChanged.connect(
            lambda: self.maskManager.BlurChange(blurIntensitySlider.value(),
                                                applyBackgroundCheck.checkState(), applyFilterCheck.checkState()))
        applyFilterCheck.stateChanged.connect(
            lambda: self.maskManager.BlurChange(blurIntensitySlider.value(),
                                                applyBackgroundCheck.checkState(), applyFilterCheck.checkState()))
        blurIntensitySlider.valueChanged.connect(
            lambda: self.maskManager.BlurChange(blurIntensitySlider.value(),
                                                applyBackgroundCheck.checkState(), applyFilterCheck.checkState()))

        #Mask manager
        self.maskManager.SetUIreferences(mainImage, currentSelectionLabel, listviewInstances,
                                         listviewClasses, listviewGroups, maskList, deleteGroupList)
        self.maskManager.ImageSelect(dropdownImages.currentText())
        self.maskManager.DrawHistogram("No filter")
        self.UpdateToneCurvePlot()

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