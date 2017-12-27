from PyQt4 import QtGui
from PyQt4 import QtCore
import cv2
import numpy as np
import platform
import os

class Visualization():
    def __init__(self, ui):
	self.ui = ui
        self.ui.runShaderButton.clicked.connect(self.runShader)

    def runShader(self):
	shader = self.ui.shaderText.toPlainText()
	f = open("shader.osl", "w")
	f.write(shader)
	f.close()
	compileLine = "oslc shader.osl > out.txt 2>&1;\n"
	print(compileLine)
	os.system(compileLine)
	f = open('out.txt', 'r')
	console = f.read()
	self.ui.visualizationOutput.setText(console)
	testShade = "testshade -g 256 256 --center -od uint8 -o Cout out.tif test"
	os.system(testShade)
	self.ui.OSLResult.setPixmap(QtGui.QPixmap("out.tif"))
	
