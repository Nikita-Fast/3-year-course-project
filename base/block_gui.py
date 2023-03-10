# базовый класс для графического представления блока.
# его задача - взять параметры от пользователя, осуществить их валидацию и передать параметры в реализацию блока
from typing import List, Dict

from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit, QAction, QToolBar, QHBoxLayout

from base.block import Block


class BlockGUI(QWidget):
    """Класс описывает графический интерфейс блока, открывающийся по двойному клику на блок, расположенный на сцене"""
    # QFormLayout

    def __init__(self, block_implementation: Block, parent=None):
        super().__init__(parent)
        self.tb_actions = {'Ok': QAction('Ok'), 'Help': QAction('Help')}
        self.tb: QToolBar = None
        self.line_edits: Dict[str, QLineEdit] = {}
        self.block_implementation = block_implementation

        self.setWindowTitle(self.__class__.__name__)
        self.setMinimumSize(300, 300)

        form_layout = QFormLayout()
        self.setLayout(form_layout)

        self.set_tool_bar()

        self.add_fields_to_form()

        self.tb.actionTriggered.connect(self.process_action)

    def process_action(self, action):
        if action == self.tb_actions['Ok']:
            """при нажатии кнопки Ок все введенные параметры передаются на валидацию"""
            self.validate_fields()
        else:
            print('This action is not implemented')

    def validate_fields(self):
        for field_name, line_edit in self.line_edits.items():
            text = line_edit.text()
            is_valid = self.block_implementation.receive_field_value_from_gui(field_name, text)
            if not is_valid:
                line_edit.setPlaceholderText('Incorrect input!')
                line_edit.clear()

    def add_fields_to_form(self):
        if self.block_implementation is not None:
            for field_name in self.block_implementation.get_field_names():
                field_value = self.block_implementation.fields[field_name].data
                line_edit = QLineEdit(str(field_value), self)
                self.line_edits[field_name] = line_edit
                self.layout().addRow(field_name, line_edit)
        self.validate_fields()

    def set_tool_bar(self):
        self.tb = QToolBar('Tools', self)
        self.tb.setAllowedAreas(Qt.TopToolBarArea)
        self.tb.addActions(list(self.tb_actions.values()))
        self.layout().setMenuBar(self.tb)

