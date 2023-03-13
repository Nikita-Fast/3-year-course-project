from typing import Dict

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

from base.base_scene_item import BaseSceneItem
from base.block import Block
from base.block_gui import BlockGUI
from utils.block_lib_parser import BlockLibParser


class MyQTreeWidgetItem(QTreeWidgetItem):

    def add_block_classes(self, block_classes: Dict):
        self.block_classes = block_classes


class BlockLibrary(QTreeWidget):

    send_scene_item = Signal(BaseSceneItem)

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
                scene_item_obj: BaseSceneItem = item.block_classes[BaseSceneItem]()
                # создаем объект реализации
                implementation_obj: Block = item.block_classes[Block]()

                # создаем gui
                gui_obj: BlockGUI = item.block_classes[BlockGUI](implementation_obj)

                # добавляем к объекту на сцене его gui
                scene_item_obj.add_gui_object(gui_obj)

                # посылаем объект на сцену
                self.send_scene_item.emit(scene_item_obj)

    def load(self):
        lib_parser = BlockLibParser()
        parsed_blocks = lib_parser.parse()
        return parsed_blocks

    def add_blocks_to_lib_gui(self):
        parsed_blocks = self.loaded

        items = []
        for block_name, block_classes_dict in parsed_blocks.items():
            item = QTreeWidgetItem([block_name])

            base_scene_item_cls = block_classes_dict[BaseSceneItem]

            child = MyQTreeWidgetItem([base_scene_item_cls.__name__])

            child.add_block_classes(block_classes_dict)

            item.addChild(child)

            items.append(item)

        self.insertTopLevelItems(0, items)

