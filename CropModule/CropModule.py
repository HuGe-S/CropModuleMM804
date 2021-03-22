import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# CropModule
#

class CropModule(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "CropModule"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Huyue Li(University of Alberta.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
"""



def createCroppedVolume(inputVolume, roi):
    cropVolumeLogic = slicer.modules.cropvolume.logic()
    cropVolumeParameterNode = slicer.vtkMRMLCropVolumeParametersNode()
    cropVolumeParameterNode.SetROINodeID(roi.GetID())
    cropVolumeParameterNode.SetInputVolumeNodeID(inputVolume.GetID())
    cropVolumeParameterNode.SetVoxelBased(True)
    cropVolumeLogic.Apply(cropVolumeParameterNode)
    croppedVolume = slicer.mrmlScene.GetNodeByID(cropVolumeParameterNode.GetOutputVolumeNodeID())
    return croppedVolume


  
class CropModuleWidget:
  def __init__(self, parent = None): #constructor 
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    # Collapsible button
    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "Main Panel"
    self.layout.addWidget(sampleCollapsibleButton)
    # Set layout

    self.formFrame = qt.QFrame(sampleCollapsibleButton)   
    self.formFrame.setLayout(qt.QHBoxLayout())
    self.formFrame1 = qt.QFrame(sampleCollapsibleButton)   
    self.formFrame1.setLayout(qt.QHBoxLayout())
    self.formFrame2 = qt.QFrame(sampleCollapsibleButton)   
    self.formFrame2.setLayout(qt.QHBoxLayout())
    self.formFrame3 = qt.QFrame(sampleCollapsibleButton)   
    self.formFrame3.setLayout(qt.QHBoxLayout())
    # bind new frame to the layout menu
    self.layout.addWidget(self.formFrame)
    self.layout.addWidget(self.formFrame1)
    self.layout.addWidget(self.formFrame2)
    self.layout.addWidget(self.formFrame3)

    #create volume selector
    self.inputSelector = qt.QLabel("Input Volume", self.formFrame)
    self.formFrame.layout().addWidget(self.inputSelector)

    self.inputSelector = slicer.qMRMLNodeComboBox(self.formFrame)
    self.inputSelector.nodeTypes = ("vtkMRMLScalarVolumeNode","")
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    #bind the current volume selector to the current scene of slicer
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    #bind the input selector to the frame
    self.formFrame.layout().addWidget(self.inputSelector)

  

    #Set up buttons
    Button_volume = qt.QPushButton("Show Volume")
    Button_volume.toolTip = "Show Volume of selected file."
    self.formFrame.layout().addWidget(Button_volume)
    Button_volume.connect('clicked(bool)', self.onButton_volumeClicked)


    Button_clip=qt.QPushButton("Crop Volume")
    Button_clip.toolTip="Crop Volume of selected file."
    self.formFrame.layout().addWidget(Button_clip)
    Button_clip.connect('clicked(bool)',self.onButton_cropClicked)


    Button_remove=qt.QPushButton("Remove Volume")
    Button_remove.toolTip="remove current scene's volume."
    self.formFrame.layout().addWidget(Button_remove)
    Button_remove.connect('clicked(bool)',self.onButton_removeClicked)

    #Set up sliders
    self.xLabel = qt.QLabel("LR", self.formFrame1)
    self.xLabel.setMinimumWidth(80)
    self.xsld = qt.QSlider(qt.Qt.Horizontal,self.formFrame1)
    self.xsld.setRange(0, 100)
    self.xsld.setValue(100) 
    self.xsld.setFixedWidth(400)
    self.xsld.setFocusPolicy(qt.Qt.NoFocus)
    self.xsld.setPageStep(5)
    self.xsld.valueChanged.connect(self.xchangeValue)
    self.xnumber = qt.QLabel('100',self.formFrame1)
    self.xnumber.setMinimumWidth(50)
    self.formFrame1.layout().addWidget(self.xLabel)
    self.formFrame1.layout().addWidget(self.xsld)
    self.formFrame1.layout().addWidget(self.xnumber)


    self.yLabel = qt.QLabel("AP", self.formFrame2)
    self.yLabel.setMinimumWidth(80)
    self.ysld = qt.QSlider(qt.Qt.Horizontal,self.formFrame2)
    self.ysld.setRange(0, 100)
    self.ysld.setValue(100) 
    self.ysld.setFixedWidth(400)
    self.ysld.setFocusPolicy(qt.Qt.NoFocus)
    self.ysld.setPageStep(5)
    self.ysld.valueChanged.connect(self.ychangeValue)
    self.ynumber = qt.QLabel('100',self.formFrame2)
    self.ynumber.setMinimumWidth(50)
    self.formFrame2.layout().addWidget(self.yLabel)
    self.formFrame2.layout().addWidget(self.ysld)
    self.formFrame2.layout().addWidget(self.ynumber)

    self.zLabel = qt.QLabel("SI", self.formFrame3)
    self.zLabel.setMinimumWidth(80)
    self.zsld = qt.QSlider(qt.Qt.Horizontal,self.formFrame3)
    self.zsld.setRange(0, 100)
    self.zsld.setValue(100) 
    self.zsld.setFixedWidth(400)
    self.zsld.setFocusPolicy(qt.Qt.NoFocus)
    self.zsld.setPageStep(5)
    self.zsld.valueChanged.connect(self.zchangeValue)
    self.znumber = qt.QLabel('100',self.formFrame3)
    self.znumber.setMinimumWidth(50)
    self.formFrame3.layout().addWidget(self.zLabel)
    self.formFrame3.layout().addWidget(self.zsld)
    self.formFrame3.layout().addWidget(self.znumber)

    #set up initial roi region
    self.x = self.xsld.value
    self.y = self.ysld.value
    self.z = self.zsld.value

    self.Button_volume = Button_volume
    self.r = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLAnnotationROINode")
    self.r.SetRadiusXYZ(100, 100, 100)
    

  def onButton_volumeClicked(self):
    '''
    show volume
    '''
    logic = slicer.modules.volumerendering.logic()
    volumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    displayNode = logic.CreateVolumeRenderingDisplayNode()
    displayNode.UnRegister(logic)
    slicer.mrmlScene.AddNode(displayNode)
    volumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
    logic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)

  def onButton_cropClicked(self):
    '''
    update volume
    '''
    r=self.r
    logic = slicer.modules.volumerendering.logic()
    volumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    cropvolumeNode = createCroppedVolume(volumeNode, r)

    slicer.mrmlScene.RemoveNode(volumeNode) 
    logic = slicer.modules.volumerendering.logic()
    displayNode = logic.CreateVolumeRenderingDisplayNode()
    displayNode.UnRegister(logic)
    slicer.mrmlScene.AddNode(displayNode)
    cropvolumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
    logic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)

  def onButton_removeClicked(self):
    '''
    remove volume
    '''
    volumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    slicer.mrmlScene.RemoveNode(volumeNode) 

  def updateLabel(self, label, value):
    '''
    update label value
    '''
    label.setText(str(value))
    self.x = self.xsld.value
    self.y = self.ysld.value
    self.z = self.zsld.value

  def xchangeValue(self, value):
    self.updateLabel(self.xnumber, value)
    self.r.SetRadiusXYZ(self.x, self.y, self.z)
    
  def ychangeValue(self, value):
    self.updateLabel(self.ynumber, value)
    self.r.SetRadiusXYZ(self.x, self.y, self.z)

  def zchangeValue(self, value):
    self.updateLabel(self.znumber, value)
    self.r.SetRadiusXYZ(self.x, self.y, self.z)


