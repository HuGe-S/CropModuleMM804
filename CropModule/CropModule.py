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

    # Layout within the sample collapsible button
    sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # Select Volume
    self.formFrame = qt.QFrame(sampleCollapsibleButton)
    # Set layout
    self.formFrame.setLayout(qt.QHBoxLayout())
    # bind new frame to the layout menu
    self.layout.addWidget(self.formFrame)

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

    # HelloWorld button
    # (Insert Section A text here)
    # (be sure to match indentation of the rest of this 
    # code)
    Button_volume=qt.QPushButton("Show Volume")
    Button_volume.toolTip="Show Volume of selected file."
    self.formFrame.layout().addWidget(Button_volume)
    Button_volume.connect('clicked(bool)',self.onButton_volumeClicked)


    Button_clip=qt.QPushButton("Crop Volume")
    Button_clip.toolTip="Show Volume of selected file."
    self.formFrame.layout().addWidget(Button_clip)
    Button_clip.connect('clicked(bool)',self.onButton_cropClicked)


    Button_remove=qt.QPushButton("Remove Volume")
    Button_remove.toolTip="remove current scene's volume."
    self.formFrame.layout().addWidget(Button_remove)
    Button_remove.connect('clicked(bool)',self.onButton_removeClicked)


    

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.Button_volume = Button_volume

    self.r=slicer.vtkMRMLAnnotationROINode()
    slicer.mrmlScene.AddNode(self.r)

  def onButton_volumeClicked(self):
    #print("Hello World !")
    #qt.QMessageBox.information(slicer.util.mainWindow(),'Slicer Python', 'Hello World!')
    logic = slicer.modules.volumerendering.logic()
    volumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    displayNode = logic.CreateVolumeRenderingDisplayNode()
    displayNode.UnRegister(logic)
    slicer.mrmlScene.AddNode(displayNode)
    volumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
    logic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)

  def onButton_cropClicked(self):
    r=self.r
    logic = slicer.modules.volumerendering.logic()
    volumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    cropvolumeNode = createCroppedVolume(volumeNode,r)

    slicer.mrmlScene.RemoveNode(volumeNode) 
    logic = slicer.modules.volumerendering.logic()
    displayNode = logic.CreateVolumeRenderingDisplayNode()
    displayNode.UnRegister(logic)
    slicer.mrmlScene.AddNode(displayNode)
    cropvolumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
    logic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)

  def onButton_removeClicked(self):
    volumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    slicer.mrmlScene.RemoveNode(volumeNode) 

