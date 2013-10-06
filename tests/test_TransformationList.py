import unittest
from ui.transformations.TransformationList import TransformationList
from vtk import *


class TransformationListTest(unittest.TestCase):

	def setUp(self):
		self.transformList = TransformationList()

	def tearDown(self):
		del self.transformList

	def testTransformationList(self):
		transform = vtkTransform()
		self.transformList.append(transform)
		self.assertEquals(len(self.transformList._transformations), 1)

		completeTransform = self.transformList.completeTransform()
		self.assertIsNotNone(completeTransform)

		matrix = completeTransform.GetMatrix()

		self.assertEquals(matrix.GetElement(0, 0), 1)
		self.assertEquals(matrix.GetElement(1, 1), 1)
		self.assertEquals(matrix.GetElement(2, 2), 1)
		self.assertEquals(matrix.GetElement(3, 3), 1)
		self.assertEquals(matrix.GetElement(1, 3), 0)

		transform = vtkTransform()
		transform.Scale(2.0, 2.0, 2.0)

		self.transformList.append(transform)
		self.assertEquals(len(self.transformList._transformations), 2)
		self.assertNotEquals(self.transformList[0], self.transformList[1])

		completeTransform = self.transformList.completeTransform()
		matrix = completeTransform.GetMatrix()
		self.assertEquals(matrix.GetElement(0, 0), 2)
		self.assertEquals(matrix.GetElement(1, 1), 2)
		self.assertEquals(matrix.GetElement(2, 2), 2)
		self.assertEquals(matrix.GetElement(3, 3), 1)
		self.assertEquals(matrix.GetElement(1, 3), 0)

		transform = vtkTransform()
		transform.Translate(3.0, 3.0, 3.0)

		self.transformList.append(transform)
		self.assertEquals(len(self.transformList._transformations), 3)
		self.assertNotEquals(self.transformList[1], self.transformList[2])

		completeTransform = self.transformList.completeTransform()
		matrix = completeTransform.GetMatrix()

		self.assertEquals(matrix.GetElement(0, 0), 2)
		self.assertEquals(matrix.GetElement(1, 1), 2)
		self.assertEquals(matrix.GetElement(2, 2), 2)
		self.assertEquals(matrix.GetElement(3, 3), 1)
		self.assertEquals(matrix.GetElement(0, 3), 3)
		self.assertEquals(matrix.GetElement(1, 3), 3)
		self.assertEquals(matrix.GetElement(2, 3), 3)

		transform = vtkTransform()
		transform.RotateX(90.0)
		
		self.transformList.append(transform)

		prevTransform = self.transformList[3]
		prevMatrix = prevTransform.GetMatrix()

		self.assertEquals(prevMatrix.GetElement(0, 0), 2)
		self.assertEquals(prevMatrix.GetElement(1, 1), 2)
		self.assertEquals(prevMatrix.GetElement(2, 2), 2)
		self.assertEquals(prevMatrix.GetElement(3, 3), 1)
		self.assertEquals(prevMatrix.GetElement(0, 3), 3)
		self.assertEquals(prevMatrix.GetElement(1, 3), 3)
		self.assertEquals(prevMatrix.GetElement(2, 3), 3)

	def testScaling(self):
		transform = vtkTransform()
		transform.Scale(3.0, 3.0, 3.0)
		transform.RotateX(45.0)
		transform.RotateY(45.0)
		transform.Translate(30, 15, 10)

		self.transformList.append(transform)

		scaleTransform = self.transformList.scalingTransform()
		scaleMatrix = scaleTransform.GetMatrix()

		self.assertAlmostEqual(scaleMatrix.GetElement(0, 0), 3, delta=0.001)
		self.assertAlmostEqual(scaleMatrix.GetElement(1, 1), 3, delta=0.001)
		self.assertAlmostEqual(scaleMatrix.GetElement(2, 2), 3, delta=0.001)
		self.assertAlmostEqual(scaleMatrix.GetElement(3, 3), 1, delta=0.001)

		transform = vtkTransform()
		transform.RotateX(45.0)
		transform.Scale(2.0, 1.0, 4.0)
		transform.Translate(30, 15, 10)
		transform.RotateY(45.0)

		self.transformList.append(transform)

		scaleTransform = self.transformList.scalingTransform()
		scaleMatrix = scaleTransform.GetMatrix()
		print scaleMatrix

		self.assertAlmostEqual(scaleMatrix.GetElement(0, 0), 10.3891, delta=0.001)
		self.assertAlmostEqual(scaleMatrix.GetElement(1, 1), 7.0356, delta=0.001)
		self.assertAlmostEqual(scaleMatrix.GetElement(2, 2), 5.6183, delta=0.001)
		self.assertAlmostEqual(scaleMatrix.GetElement(3, 3), 1.0000, delta=0.001)

		comp = self.transformList.completeTransform()
		print comp.GetMatrix()

		self.assertFalse(True)

		# ShearX: 3.99680288865e-15
		# ShearY: -3.99680288865e-15
		# ShearZ: 1.24344978758e-14
		# ShearX: -55.6378246381
		# ShearY: 1.63782463806
		# ShearZ: 20.25
