import inspect
# from lib.binary_generator import binary_generator_scene_item
import os
# from lib.binary_generator.binary_generator_scene_item import *
import sys
from enum import Enum
from typing import List

from base_scene_item import BaseSceneItem
from block_gui import BlockGUI


class BlockLibParser:
    """Класс отвечающий за парсинг библиотечных блоков"""

    def __init__(self, block_requirements: List):
        """Конструктор

            Parameters
            __________
            block_requirements: List
                Список классов, которые должны быть реализованы в наборе файлов, описывающих блок
            """
        self.block_requirements = block_requirements

    def parse(self):
        parsed_blocks = {}
        directory = 'lib'
        for folder_name in os.listdir(directory):
            folder = os.path.join(directory, folder_name)
            if os.path.isdir(folder):
                print(folder_name)

                requirements_implementation = self.parse_folder(folder)
                if requirements_implementation is not None:
                    parsed_blocks[folder_name] = requirements_implementation
        return parsed_blocks


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

    def parse_folder(self, dir_path: str):
        """Если в папке есть набор файлов, содержащие все необходимые для описания блока классы
        (эти классы перечисленны в readme.txt), то добавляем классы в словарь, чтобы потом можно было
        подргузить в либу блоков"""

        satisfied_requirements = {cls: None for cls in self.block_requirements}
        classes = []

        if not os.path.isdir(dir_path):
            raise Exception('переданный путь должен указывать на папку')
        for file_name in os.listdir(dir_path):
            file = os.path.join(dir_path, file_name)
            if BlockLibParser.is_python_file(file):
                file = BlockLibParser.prepare_py_file_for_import(file)
                exec('import ' + file)
                classes = BlockLibParser.get_classes_from_module(file)

                for cls in classes:
                    for req_cls in self.block_requirements:
                        if req_cls in cls.__bases__:
                            satisfied_requirements[req_cls] = cls

        if all(v is not None for v in satisfied_requirements.values()):
            print('папка %s содержит все нужные файлы' % dir_path)
            return satisfied_requirements
        else:
            return None
