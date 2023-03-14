from typing import Dict

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

from base.block.block_scene_item import BlockSceneItem
from base.block.block_description import BlockDescription
from base.block.block_gui import BlockGUI
from utils.block_lib_loader import BlockLibLoader


class MyQTreeWidgetItem(QTreeWidgetItem):

    def add_block_classes(self, block_classes: Dict):
        self.block_classes = block_classes


class BlockLibrary(QTreeWidget):

    send_scene_item = Signal(BlockSceneItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.setHeaderLabel('Block name')

        self.loaded = self.load()
        self.add_blocks_to_lib_gui()

        self.itemDoubleClicked.connect(self.on_double_click)
        self.setMinimumSize(200, 300)

    def on_double_click(self, item: QTreeWidgetItem, column):
        if item is not None and item.childCount() == 0:
            if isinstance(item, MyQTreeWidgetItem):
                # создаем объект для сцены
                scene_item_obj: BlockSceneItem = item.block_classes[BlockSceneItem]()
                # создаем объект реализации
                implementation_obj: BlockDescription = item.block_classes[BlockDescription]()

                # создаем gui
                gui_obj: BlockGUI = item.block_classes[BlockGUI](implementation_obj)

                # добавляем к объекту на сцене его gui
                scene_item_obj.add_gui_object(gui_obj)

                # посылаем объект на сцену
                self.send_scene_item.emit(scene_item_obj)

    def load(self):
        lib_parser = BlockLibLoader()
        parsed_blocks = lib_parser.parse()
        return parsed_blocks

    def add_blocks_to_lib_gui(self):
        parsed_blocks = self.loaded

        items = []
        for block_name, block_classes_dict in parsed_blocks.items():
            item = QTreeWidgetItem([block_name])

            base_scene_item_cls = block_classes_dict[BlockSceneItem]

            child = MyQTreeWidgetItem([base_scene_item_cls.__name__])

            child.add_block_classes(block_classes_dict)

            item.addChild(child)

            items.append(item)

        self.insertTopLevelItems(0, items)

