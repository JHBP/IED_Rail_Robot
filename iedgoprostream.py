# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
from time import sleep
import Tkinter as tki
import threading
import datetime
import cv2
import os

class IEDGUI:
	def __init__(self, cvv, outputPath):
		######################INITIALIZE VALUES########################
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		# initialize the root window and image panel
		# store the video stream object and output path, then initialize
		self.outputPath = outputPath
		self.frame = None
		self.ret = None
		self.thread = None
		self.stopEvent = None
		self.record = False
		self.root = tki.Tk()
		self.panel = None
		self.cvv = cvv
		self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.fwidth = self.cvv.get(3)
		self.fheight = self.cvv.get(4)
		self.filename = None
		self.p = None
		self.out = None#out flag
		self.save = 0#save flag
		##############################BUTTONS############################
		# create a button, that when pressed, will take the current
		# frame and save it to file
		#snap shot button
		btnss = tki.Button(self.root, text="Snapshot!",	command=self.takeSnapshot)
		btnss.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
		#video pause and save button
		btnv = tki.Button(self.root, text="Stop",bg="black",fg="white", command=self.stopRecording)
		btnv.pack(side="right", padx=10, pady=10)
		#video record button
		btnv = tki.Button(self.root, text="Record",bg="red",fg="white", command=self.startRecording)
		btnv.pack(side="right", padx=10, pady=10)
		
		#########################THREADING##################################
		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
		# set a callback to handle when the window is closed
		self.root.wm_title("I-Beam Monitor")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
	####################FUNCTIONS#####################

	def videoLoop(self):
		try:
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():
				# grab the frame from the Open CV
				self.ret,self.frame = self.cvv.read()
				# OpenCV represents images in BGR order; however PIL
				# represents images in RGB order, so we need to swap
				# the channels, then convert to PIL and ImageTk format
				if self.ret==True:
					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)
			
					# if the panel is not None, we need to initialize it
					if self.panel is None:
						self.panel = tki.Label(image=image)
						self.panel.image = image
						self.panel.pack(side="top", padx=10, pady=10)
			
					# otherwise, simply update the panel
					else:
						self.panel.configure(image=image)
						self.panel.image = image
					if self.record == True:
						self.save=1
						ret,frame = self.cvv.read()
						if ret==True and self.out!= None:
							self.out.write(frame)
					elif self.record == False and self.save == 1:
						print("[INFO] saved {}".format(self.filename))
						self.out.release()
						self.save=0
						self.out = None	

		except RuntimeError, e:
			print("[INFO] caught a RuntimeError")

	def takeSnapshot(self):
		# grab the current timestamp and use it to construct the
		# output path
		ts = datetime.datetime.now()
		filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		p = os.path.sep.join((self.outputPath, filename))

		# save the file
		cv2.imwrite(p, self.frame.copy())
		print("[INFO] saved {}".format(filename))

	def startRecording(self):
		print("start recording...")
		self.record = True
		ts = datetime.datetime.now()
		self.filename = "{}.avi".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		self.p = os.path.sep.join((self.outputPath, self.filename))
		self.out = cv2.VideoWriter(self.p,self.fourcc,  20.0, (int(self.fwidth),int(self.fheight)))
	
	def stopRecording(self):
		print("stop recording.")
		self.record = False 

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.cvv.release()
		sleep(.5)
		self.root.destroy()


		