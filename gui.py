# графический итерфейс для создания модели и работы с ней
# состоит из:
# 1) список доступных блоков
# 2) сцены
# 3) панели инструментов
# 4) панели состояния

from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QGraphicsView, QDockWidget, QToolBar

from base_scene_item import BaseSceneItem
from block_gui import BlockGUI
from block_lib_parser import BlockLibParser
from block_library import BlockLibrary
from graphics_scene import BaseGraphicsScene
from menu_bar import MenuBar
from tool_bar import ToolBar


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.show()
        self.add_graphics_scene()
        self.add_tool_bar()
        self.add_menu_bar()
        self.add_block_library()

    def add_graphics_scene(self):
        self.scene = BaseGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 2000, 2000)
        self.setCentralWidget(self.view)

    def add_tool_bar(self):
        tool_bar = ToolBar()
        self.addToolBar(tool_bar)

    def add_menu_bar(self):
        menu_bar = MenuBar()
        self.setMenuBar(menu_bar)

    def add_block_library(self):
        block_lib = BlockLibrary()
        dock_block_lib = QDockWidget()
        dock_block_lib.setWidget(block_lib)
        dock_block_lib.setAllowedAreas(Qt.LeftDockWidgetArea)
        dock_block_lib.setWindowTitle('Library')
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_block_lib)

        # block_lib.itemDoubleClicked.connect(self.scene.helper)
        block_lib.item_double_clicked.connect(self.scene.add_block)

    def add_status_bar(self, status_bar):
        pass

