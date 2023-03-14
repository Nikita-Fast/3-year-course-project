# базовый класс для графического представления блока.
# его задача - взять параметры от пользователя, осуществить их валидацию и передать параметры в реализацию блока
from typing import Dict

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit, QAction, QToolBar

from base.block.block_description import BlockDescription


class BlockGUI(QWidget):
    """Класс описывает графический интерфейс блока, открывающийся по двойному клику на блок, расположенный на сцене"""
    # QFormLayout

    def __init__(self, block_implementation: BlockDescription, parent=None):
        super().__init__(parent)
        self.tb_actions = {'Ok': QAction('Ok'), 'Help': QAction('Help')}
        self.tb: QToolBar = None
        self.line_edits: Dict[str, QLineEdit] = {}
        self.block_description = block_implementation

        self.setWindowTitle(self.__class__.__name__)
        self.setMinimumSize(300, 300)

        form_layout = QFormLayout()
        self.setLayout(form_layout)

        self.set_tool_bar()

        self.add_params_to_form()

        self.tb.actionTriggered.connect(self.process_action)

    def process_action(self, action):
        if action == self.tb_actions['Ok']:
            """при нажатии кнопки Ок все введенные параметры передаются на валидацию"""
            self.validate_params()
        else:
            print('This action is not implemented')

    def validate_params(self):
        # todo отвязаться от line edit-a
        for param_name, line_edit in self.line_edits.items():
            text = line_edit.text()
            is_valid = self.block_description.receive_param_value_from_gui(param_name, text)
            if not is_valid:
                line_edit.setPlaceholderText('Incorrect input!')
                line_edit.clear()

    def add_params_to_form(self):
        if self.block_description is not None:
            for param_name in self.block_description.get_param_names():
                param_value = self.block_description.params[param_name].data
                line_edit = QLineEdit(str(param_value), self)
                self.line_edits[param_name] = line_edit
                self.layout().addRow(param_name, line_edit)
        self.validate_params()

    def set_tool_bar(self):
        self.tb = QToolBar('Tools', self)
        self.tb.setAllowedAreas(Qt.TopToolBarArea)
        self.tb.addActions(list(self.tb_actions.values()))
        self.layout().setMenuBar(self.tb)

