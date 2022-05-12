from maya import cmds
from PySide2 import QtWidgets, QtGui, QtCore

class LOD():
    def __init__(self, lod_list = []):
        self.camera = cmds.camera(name='LOD_camera')
        self.lod_list = lod_list
        self.distance = None
    
    def set_distance(self):
        if(cmds.objExists('distanceBetween1') != True):
            self.distance = cmds.shadingNode('distanceBetween', asUtility = True)
            cmds.connectAttr(f'{self.camera[0]}.translate', f'{self.distance}.point1', f=True)
            translate = f'{self.lod_list[0]}.translate'
            cmds.connectAttr(translate, f'{self.distance}.point2', f=True)


class LODController():
    def __init__(self):
        pass

    def organize(self, lod_list):
        group_list = []
        for x in lod_list:
            group_list.append(cmds.group(x, n=f'LOD_{lod_list.index(x)}'))
            print(f'grouped: {x}')
        print(f'groupList: {group_list}')
        cmds.group(group_list, n='LOD_Group')
    
    
    def link_lod_cam(self, lod, distance=False, percentage=False):
        cmds.lookThru(lod.camera)
        lod.setDistance()
        if distance:
            pass
            # print(f'distance: {distance}')
        elif percentage:
            pass
            # print(f'percentage: {percentage}')

class LODUI(QtWidgets.QDialog):
    def __init__(self):
        super(LODUI, self).__init__()
        self.setWindowTitle("Level Of Detail Tool")
        self.setFixedSize(QtCore.QSize(600,700))
        
        # controller logic
        self.library = LODController()

        # global widgets
        self.lod_list = QtWidgets.QListWidget()
        self.lod_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.lod_list.setAlternatingRowColors(True)
        self.lod_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.camera_combobox = QtWidgets.QComboBox()

        self.populate_cam_list()
        self.build_ui()

    def build_ui(self):
        # layouts
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout_1 = QtWidgets.QHBoxLayout()
        h_layout_2 = QtWidgets.QHBoxLayout()
        h_layout_3 = QtWidgets.QHBoxLayout()

        # widgets
        prompt_1 = QtWidgets.QLabel('Add and Arrange LOD Models from most to least detailed')
        add_button = QtWidgets.QPushButton('Add')
        remove_button = QtWidgets.QPushButton('Remove')
        refresh_button = QtWidgets.QPushButton('Refresh')
        create_button = QtWidgets.QPushButton('Create')
        interval_prompt = QtWidgets.QLabel('Distance Interval')
        interval_spinbox = QtWidgets.QSpinBox()
        self.distance_checkbox = QtWidgets.QCheckBox('Distance')
        self.distance_checkbox.setCheckState(QtCore.Qt.Checked)
        self.percentage_checkbox = QtWidgets.QCheckBox('Screen Height Percentage')


        # signals
        add_button.clicked.connect(self.add_list_items)
        remove_button.clicked.connect(self.remove_list_items)
        refresh_button.clicked.connect(self.populate_cam_list)
        create_button.clicked.connect(self.create_lod_cam)
        self.distance_checkbox.stateChanged.connect(self.distance_state)
        self.percentage_checkbox.stateChanged.connect(self.percentage_state)

        v_layout.addWidget(prompt_1)
        v_layout.addWidget(self.lod_list)
        v_layout.addLayout(h_layout_1)
        v_layout.addWidget(QtWidgets.QSplitter(QtCore.Qt.Horizontal))
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)

        h_layout_1.addWidget(add_button)
        h_layout_1.addWidget(remove_button)


        h_layout_2.addWidget(interval_prompt)
        h_layout_2.addWidget(interval_spinbox)
        h_layout_2.addWidget(self.distance_checkbox)
        h_layout_2.addWidget(self.percentage_checkbox)
        
        h_layout_3.addWidget(create_button)
        h_layout_3.addWidget(refresh_button)
        h_layout_3.addWidget(self.camera_combobox)

    def distance_state(self, s):
        if s == QtCore.Qt.Checked:
            self.percentage_checkbox.setCheckState(QtCore.Qt.Unchecked)

    def percentage_state(self, s):
        if s == QtCore.Qt.Checked:
            self.distance_checkbox.setCheckState(QtCore.Qt.Unchecked)

    def add_list_items(self):
        selections = cmds.ls(selection=True)
        for selection in selections:
            # if it doesn't find a duplicate
            if not self.lod_list.findItems(selection, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchCaseSensitive):
                self.lod_list.addItem(selection)
            else:
                print(f'duplicate detected')
    
    def remove_list_items(self):
        list_items = self.lod_list.selectedItems()
        if not list_items: return
        for item in list_items:
            self.lod_list.takeItem(self.lod_list.row(item))

    def create_lod_cam(self):
        if(self.camera_combobox.currentText() == 'Create New Camera'):
            list_items = []
            for x in range(self.lod_list.count()):
                list_items.append(self.lod_list.item(x).text())
            self.library.organize(list_items)
            self.lod = LOD(list_items)
            self.library.link_lod_cam(self.lod, self.distance_checkbox.isChecked(), self.percentage_checkbox.isChecked())
            self.populate_cam_list()
            self.lod_list.clear()

        else:
            print(f'current camera: {self.camera_combobox.currentText}')
        
    def populate_cam_list(self):
        self.camera_combobox.clear()
        camera_list = cmds.listCameras()
        print(f'repopulate: {camera_list}')
        self.camera_combobox.addItem('Create New Camera')
        self.camera_combobox.addItems(camera_list)

def show_ui():
    ui = LODUI()
    ui.show()
    return ui

ui = show_ui()