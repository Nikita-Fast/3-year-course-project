import inspect
# from lib.binary_generator import binary_generator_scene_item
import os
# from lib.binary_generator.binary_generator_scene_item import *
import sys
from typing import List

from base.block.block_implementation import BlockImplementation
from base.block.block_scene_item import BlockSceneItem
from base.block.block_description import BlockDescription
from base.block.block_gui import BlockGUI


class BlockLibLoader:
    """Класс отвечающий за парсинг библиотечных блоков"""

    def __init__(self, block_requirements: List = None):
        """Конструктор

            Parameters
            __________
            block_requirements: List
                Список классов, которые должны быть реализованы в наборе файлов, описывающих блок
            """
        if block_requirements is None:
            block_requirements = BlockLibLoader.default_block_requirements()

        self.block_requirements = block_requirements

    def parse(self):
        parsed_blocks = {}
        directory = 'lib'
        for folder_name in os.listdir(directory):
            folder = os.path.join(directory, folder_name)
            if os.path.isdir(folder):

                requirements_implementation = self.parse_folder(folder)
                if requirements_implementation is not None:
                    parsed_blocks[folder_name] = requirements_implementation
        return parsed_blocks

    @staticmethod
    def default_block_requirements():
        return [BlockDescription, BlockGUI, BlockSceneItem, BlockImplementation]

    @staticmethod
    def is_python_file(file: str):
        return file.endswith('.py')

    @staticmethod
    def prepare_py_file_for_import(file: str):
        return file.split(sep='.')[0].replace('/', '.')

    @staticmethod
    def get_classes_from_module(file: str):
        return [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules[file]) if
                inspect.isclass(cls_obj)]

    @staticmethod
    def import_py_file(file: str):
        exec('import ' + file)

    @staticmethod
    def find_implementation_cls(folder_path: str):
        if not os.path.isdir(folder_path):
            raise Exception('путь должен указывать на папку')
        for file_name in os.listdir(folder_path):
            file = os.path.join(folder_path, file_name)
            if BlockLibLoader.is_python_file(file):
                file = BlockLibLoader.prepare_py_file_for_import(file)
                BlockLibLoader.import_py_file(file)
                classes = BlockLibLoader.get_classes_from_module(file)

                for cls in classes:
                    if BlockImplementation in cls.__bases__:
                        return cls


    def parse_folder(self, dir_path: str):
        """Если в папке есть набор файлов, содержащие все классы необходимые для описания блока
        (эти классы перечисленны в self.block_requirements), то добавляем классы в словарь, чтобы потом можно было
        подргузить в либу блоков"""

        satisfied_requirements = {cls: None for cls in self.block_requirements}
        classes = []

        if not os.path.isdir(dir_path):
            raise Exception('переданный путь должен указывать на папку')
        for file_name in os.listdir(dir_path):
            file = os.path.join(dir_path, file_name)
            if BlockLibLoader.is_python_file(file):
                file = BlockLibLoader.prepare_py_file_for_import(file)
                BlockLibLoader.import_py_file(file)
                classes = BlockLibLoader.get_classes_from_module(file)

                for cls in classes:
                    for req_cls in self.block_requirements:
                        if req_cls in cls.__bases__:
                            satisfied_requirements[req_cls] = cls

        if all(cls is not None for cls in satisfied_requirements.values()):
            return satisfied_requirements
        else:
            return None
