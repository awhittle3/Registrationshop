"""
RenderWidget

:Authors:
	Berend Klein Haneveld
"""

from vtk import vtkRenderer
from vtk import vtkVolume
from vtk import vtkInteractorStyleTrackballCamera
from vtk import vtkOpenGLGPUVolumeRayCastMapper
from vtk import vtkVersion
from vtk import vtkOrientationMarkerWidget
from vtk import vtkAxesActor
from vtk import vtkImagePlaneWidget
from PySide.QtGui import QGridLayout
from PySide.QtGui import QWidget
from PySide.QtCore import Signal
from PySide.QtCore import Slot
from ui.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

VTK_MAJOR_VERSION = vtkVersion.GetVTKMajorVersion()

class RenderWidget(QWidget):
	"""
	RenderWidget for rendering volumes. It has a few render types which can be
	set and adjusted.
	"""

	dataChanged = Signal()
	updated = Signal()

	def __init__(self):
		super(RenderWidget, self).__init__()

		self.renderer = vtkRenderer()
		self.renderer.SetBackground2(0.4, 0.4, 0.4)
		self.renderer.SetBackground(0.1, 0.1, 0.1)
		self.renderer.SetGradientBackground(True)

		self.rwi = QVTKRenderWindowInteractor(parent=self)
		self.rwi.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
		self.rwi.GetRenderWindow().AddRenderer(self.renderer)

		self.imagePlaneWidgets = [vtkImagePlaneWidget() for i in range(3)]
		for index in range(3):
			self.imagePlaneWidgets[index].DisplayTextOn()
			self.imagePlaneWidgets[index].SetInteractor(self.rwi)

		self.volume = None
		self.mapper = vtkOpenGLGPUVolumeRayCastMapper()
		self.imageData = None
		self.volumeProperty = None
		self.shouldResetCamera = False

		axesActor = vtkAxesActor();
		self.orientationWidget = vtkOrientationMarkerWidget()
		self.orientationWidget.SetViewport(0.05, 0.05, 0.3, 0.3)
		self.orientationWidget.SetOrientationMarker(axesActor)
		self.orientationWidget.SetInteractor(self.rwi)
		self.orientationWidget.EnabledOn()
		self.orientationWidget.InteractiveOff()

		layout = QGridLayout(self)
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self.rwi, 0, 0)
		self.setLayout(layout)

	def render(self):
		if self.shouldResetCamera:
			self.renderer.ResetCamera()
			self.shouldResetCamera = False
		self.rwi.Render()

	@Slot(object)
	def setData(self, imageData):
		"""
		Updates the image data. If the image data is none, then
		the volume gets removed from the renderer. Otherwise, the
		new image data is given to the mapper.
		"""
		self.imageData = imageData
		if self.imageData is None:
			if self.volume is not None:
				self.renderer.RemoveViewProp(self.volume) 
			print "Warning: image data is None"
			self.render()
			return

		# Set the image data for the mapper
		if VTK_MAJOR_VERSION <= 5:
			self.mapper.SetInput(self.imageData)
		else:
			self.mapper.SetInputData(self.imageData)

		# Set the image data for the slices
		for index in range(3):
			if VTK_MAJOR_VERSION <= 5:
				self.imagePlaneWidgets[index].SetInput(self.imageData)
			else:
				self.imagePlaneWidgets[index].SetInputData(self.imageData)
			self.imagePlaneWidgets[index].SetPlaneOrientation(index)

		self.shouldResetCamera = True
		# Don't call render, because camera should only be reset
		# when a volume property is loaded

	@Slot(object)
	def setVolumeProperty(self, volumeProperty):
		"""
		Updates the volume property. It actually removes the volume, 
		creates a new volume and sets the updated volume property and
		then adds the new volume to the renderer.
		Just updating the vtkVolumeProperty gives artifacts and seems
		to not work correctly.
		:type volumeProperty: VolumeProperty
		"""
		self.volumeProperty = volumeProperty

		if self.volume is not None:
			self.renderer.RemoveViewProp(self.volume)
			self.volume = None

		if self.imageData is None or self.volumeProperty is None:
			print "Warning: image data or volume property is None"
			return

		# Do the mapper stuff here!
		assert self.volume is None
		self.volume = vtkVolume()
		self.volume.SetProperty(self.volumeProperty.volumeProperty)
		self.volume.SetMapper(self.mapper)
		self.renderer.AddViewProp(self.volume)
		
		self.render()
		

	@Slot(object)
	def setSlices(self, slices):
		for sliceIndex in range(len(slices)):
			if slices[sliceIndex]:
				self.imagePlaneWidgets[sliceIndex].On()
			else:
				self.imagePlaneWidgets[sliceIndex].Off()