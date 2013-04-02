import unittest
import os
import shutil
from core.elastix.Elastix import Elastix
from core.elastix.ElastixCommand import ElastixCommand


class ElastixTest(unittest.TestCase):

	def setUp(self):
		self.elastix = Elastix()

	def tearDown(self):
		del self.elastix

	def testElastix(self):
		self.assertIsNotNone(self.elastix)
		# self.assertFalse(self.elastix.processing)
		# self.assertIsNone(self.elastix.currentTask)

	def testProcessingSingleTask(self):
		if not hasattr(self, "path"):
			# Get the path of the current test
			self.path = os.path.dirname(os.path.abspath(__file__))
		
		# Create paths to some data sets
		movingData = self.path + "/data/hi-5.mhd"
		fixedData = self.path + "/data/hi-3.mhd"
		outputFolder = self.path + "/data/output"
		transformation = self.path + "/data/Sample.txt"

		# Construct a simple valid command object
		command = ElastixCommand(fixedData=fixedData, 
								 movingData=movingData, 
								 outputFolder=outputFolder, 
								 transformation=transformation)

		self.assertTrue(command.isValid())

		self.elastix.process(command)

		# Important parameters to keep track of:
		# (NumberOfResolutions 1)
		# (MaximumNumberOfIterations 50)
		# These are the most time consuming operations within Elastix and 
		# are a good way of keeping track of the process.

		# self.assertTrue(task.finished)
		self.assertTrue(os.path.exists(outputFolder + "/result.0.mhd"))

		# Cleanup test directory
		try:
			if os.path.exists(outputFolder):
				shutil.rmtree(outputFolder)
		except Exception, e:
			raise e

	def testProcessingInvalidTaskRaisesException(self):
		# Create incomplete task (is missing command)
		otherTask = ElastixCommand()
		
		self.assertRaises(Exception, self.elastix.process, otherTask)

	# def testAddingTaskToQueue(self):
	# 	task = ElastixTask()

	# 	self.assertFalse(self.elastix.processing)
	# 	self.assertEqual(len(self.elastix.queue), 0)
	# 	self.elastix.addTask(task)
	# 	self.assertEqual(len(self.elastix.queue), 1)
	# 	self.assertFalse(self.elastix.processing)

	# def testAddingDuplicateTasks(self):
	# 	task = ElastixTask()

	# 	self.assertEqual(len(self.elastix.queue), 0)
	# 	self.elastix.addTask(task)
	# 	self.elastix.addTask(task)
	# 	self.assertEqual(len(self.elastix.queue), 1)
		
	# def testCancelTask(self):
	# 	task = ElastixTask()
	# 	self.elastix.addTask(task)

	# 	self.assertEqual(len(self.elastix.queue), 1)
	# 	self.elastix.cancelTask(task)
	# 	self.assertEqual(len(self.elastix.queue), 0)

	# def testStartAndStopProcessing(self):
	# 	self.assertFalse(self.elastix.processing)
	# 	self.elastix.startProcessing()
	# 	self.assertTrue(self.elastix.processing)

	# 	self.elastix.stopProcessing()
	# 	self.assertFalse(self.elastix.processing)

	
