# графический итерфейс для создания модели и работы с ней
# состоит из:
# 1) библиотеки блоков
# 2) сцены
# 3) панели инструментов
# 4) панели состояния

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QGraphicsView, QDockWidget

from main_window_gui.block_library import BlockLibrary
from main_window_gui.graphics_scene import BaseGraphicsScene
from main_window_gui.menu_bar import MenuBar
from main_window_gui.status_bar import StatusBar
from main_window_gui.tool_bar import ToolBar


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle('Simulink')
        self.show()
        self.add_graphics_scene()
        self.add_tool_bar()
        self.add_menu_bar()
        self.add_block_library()
        self.add_status_bar()

        self.tool_bar.actionTriggered.connect(self.tool_bar_action_handler)

    def tool_bar_action_handler(self, action):
        if action.text() == 'пыщ':
            self.magic_button_clicked()

    def magic_button_clicked(self):
        """запустить валидацию модели.
        Пока что только блоков, все их поля должны иметь валидные значения
        """

        # todo кошмарный доступ к имплементации
        if all(b.gui.block_implementation.is_each_field_has_valid_value() for b in self.scene.blocks):
            self.statusBar().showMessage('Модель валидна', 5000)

    def add_graphics_scene(self):
        self.scene = BaseGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 2000, 2000)
        self.view.setMinimumSize(500, 400)
        self.setCentralWidget(self.view)

    def add_tool_bar(self):
        self.tool_bar = ToolBar()
        self.addToolBar(self.tool_bar)

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

        block_lib.send_scene_item.connect(self.scene.add_block)

    def add_status_bar(self):
        self.setStatusBar(StatusBar())
        self.statusBar().showMessage('Model status')

