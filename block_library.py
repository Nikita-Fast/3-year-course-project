from typing import Any

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

from base_scene_item import BaseSceneItem
from block_gui import BlockGUI
from block_lib_parser import BlockLibParser
from lib.binary_generator.binary_generator_scene_item import BinaryGeneratorSceneItem


class MyQTreeWidgetItem(QTreeWidgetItem):

    def add_ref(self, base_scene_item_impl):
        self.ref = base_scene_item_impl

class BlockLibrary(QTreeWidget):

    item_double_clicked = Signal(BaseSceneItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.setHeaderLabel('Block name')

        self.loaded = self.load()
        self.add_blocks_to_lib_gui()

        self.itemDoubleClicked.connect(self.on_double_click)

    def on_double_click(self, item: QTreeWidgetItem, column):
        if item is not None and item.childCount() == 0:
            if isinstance(item, MyQTreeWidgetItem):
                self.item_double_clicked.emit(item.ref())

    def load(self):
        lib_parser = BlockLibParser([BaseSceneItem, BlockGUI])
        parsed_blocks = lib_parser.parse()
        return parsed_blocks

    def add_blocks_to_lib_gui(self):
        parsed_blocks = self.loaded

        items = []
        for block_name, block_classes_dict in parsed_blocks.items():
            item = QTreeWidgetItem([block_name])

            base_scene_item_cls = block_classes_dict[BaseSceneItem]
            child = MyQTreeWidgetItem([base_scene_item_cls.__name__])
            child.add_ref(base_scene_item_cls)
            # child = QTreeWidgetItem([base_scene_item_cls.__name__])
            item.addChild(child)

            items.append(item)

        self.insertTopLevelItems(0, items)

