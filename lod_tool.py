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

        self.lodList = QtWidgets.QListWidget()
        self.lodList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.lodList.setAlternatingRowColors(True)
        self.lodList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.cameraComboBox = QtWidgets.QComboBox()

        self.populateCamList()
        self.buildUI()

    def buildUI(self):
        # layouts
        Vlayout = QtWidgets.QVBoxLayout(self)
        Hlayout1 = QtWidgets.QHBoxLayout()
        Hlayout2 = QtWidgets.QHBoxLayout()

        # widgets
        prompt1 = QtWidgets.QLabel('Add and Arrange LOD Models from most to least detailed')
        addButton = QtWidgets.QPushButton('Add')
        removeButton = QtWidgets.QPushButton('Remove')
        refreshButton = QtWidgets.QPushButton('Refresh')
        createButton = QtWidgets.QPushButton('Create')

        # signals
        addButton.clicked.connect(self.addListItems)
        removeButton.clicked.connect(self.removeListItems)
        refreshButton.clicked.connect(self.populateCamList)
        createButton.clicked.connect(self.createLodCam)

        Vlayout.addWidget(prompt1)
        Vlayout.addWidget(self.lodList)
        Vlayout.addLayout(Hlayout1)
        Vlayout.addLayout(Hlayout2)

        Hlayout1.addWidget(addButton)
        Hlayout1.addWidget(removeButton)
        
        Hlayout2.addWidget(createButton)
        Hlayout2.addWidget(refreshButton)
        Hlayout2.addWidget(self.cameraComboBox)

    def addListItems(self):
        selections = cmds.ls(selection=True)
        for selection in selections:
            # if it doesn't find a duplicate
            if not self.lodList.findItems(selection, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchCaseSensitive):
                self.lodList.addItem(selection)
            else:
                print(f'duplicate detected')
    
    def removeListItems(self):
        listItems = self.lodList.selectedItems()
        if not listItems: return
        for item in listItems:
            self.lodList.takeItem(self.lodList.row(item))

    def createLodCam(self):
        if(self.cameraComboBox.currentText() == 'Create New Camera'):
            cmds.camera(name='LodCam')
            self.populateCamList()
        else:
            print(f'current camera: {self.cameraComboBox.currentText}')
        
    def populateCamList(self):
        self.cameraComboBox.clear()
        cameralist = cmds.listCameras()
        print(f'repopulate: {cameralist}')
        self.cameraComboBox.addItem('Create New Camera')
        self.cameraComboBox.addItems(cameralist)

def showUI():
    ui = LODUI()
    ui.show()
    return ui

ui = showUI()