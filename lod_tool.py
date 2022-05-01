from maya import cmds
from PySide2 import QtWidgets, QtGui, QtCore

class LODController():
    pass

class LODUI(QtWidgets.QDialog):
    def __init__(self):
        super(LODUI, self).__init__()
        self.setWindowTitle("Level Of Detail Tool")
        self.setFixedSize(QtCore.QSize(600,700))
        
        self.library = LODController()
        self.buildUI()

    def buildUI(self):
        # layouts
        Vlayout = QtWidgets.QVBoxLayout(self)
        Hlayout1 = QtWidgets.QHBoxLayout()
        Hlayout2 = QtWidgets.QHBoxLayout()

        # widgets
        prompt1 = QtWidgets.QLabel('Add and Arrange LOD Models from most to least detailed')
        lodList = QtWidgets.QListWidget()
        addButton = QtWidgets.QPushButton('Add')
        removeButton = QtWidgets.QPushButton('Remove')
        createButton = QtWidgets.QPushButton('Create')
        cameraComboBox = QtWidgets.QComboBox()

        Vlayout.addWidget(prompt1)
        Vlayout.addWidget(lodList)
        Vlayout.addLayout(Hlayout1)
        Vlayout.addLayout(Hlayout2)

        Hlayout1.addWidget(removeButton)
        Hlayout1.addWidget(addButton)
        
        Hlayout2.addWidget(createButton)
        Hlayout2.addWidget(cameraComboBox)
        

def showUI():
    ui = LODUI()
    ui.show()
    return ui

ui = showUI()