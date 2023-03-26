from typing import List, Dict

from base.block.block_scene_item import BlockSceneItem
from base.connection.connection_scene_item import ConnectionSceneItemDraft
from base.port.port_scene_item import PortSceneItem
from base.port.port_type import PortType
from utils.block_lib_loader import BlockLibLoader
from utils.parameter import Parameter


class NaiveCodeGenerator:

    def __init__(self):
        # в моделе все блоки хранятся в списке с именем list_name,
        # можно сопоставить BlockSceneItem-у позицию ассоциированного с ним блока
        # в списке с именем list_name
        self.block_var_names = []
        self.scene_connection_to_var_name: Dict[ConnectionSceneItemDraft, str] = {}
        self.scene_block_to_var_name: Dict[BlockSceneItem, str] = {}
        self.block_list_name = None
        self.scene_block_to_block_number: Dict[BlockSceneItem, int] = {}

    def generate_code(self, blocks: List[BlockSceneItem], params: List[List[Parameter]]) -> str:
        # в сгенерированном коде созданные блоки будут храниться в списке с таким именем
        # self.block_list_name = 'blocks'
        # генерируемые строчки кода
        code_lines = ['from matplotlib import pyplot as plt']

        # генерируем импорт классов для блоков
        for b in blocks:
            code_lines.append(NaiveCodeGenerator.gen_block_import(b))

        code_lines.append(NaiveCodeGenerator.gen_connection_import())

        # создаем блоки и сохраняем их в переменные
        code_lines.append('')
        for i in range(len(blocks)):
            b = blocks[i]
            b_params = params[i]
            s = self.gen_block_creation2(b, b_params)
            code_lines.append(s)

        # создаем список со всеми блоками
        code_lines.append(
            'blocks = [{}]'.format(', '.join(self.block_var_names))
        )

        # connections
        code_lines.append('')
        for b in blocks:
            for port in b.inputs + b.outputs:
                if port.is_connected():
                    print('connected port')
                    if port.connection not in self.scene_connection_to_var_name:
                        s = self.gen_connection_construction(port.connection)
                        code_lines.append(s)

        # моделирование
        code_lines.append('')
        code_lines.append('ebn0_max = 10')
        code_lines += NaiveCodeGenerator.gen_modelling_code('ebn0_max', 'const0')

        # построение ber_plot
        code_lines.append('')
        code_lines += NaiveCodeGenerator.gen_ber_plotting('accumulator0.acc')

        return '\n'.join(code_lines)

    @staticmethod
    def gen_ber_plotting(ber_points_storage_name: str):
        return ['plt.yscale("log")',
                'plt.grid(visible=\'true\')',
                'plt.xlabel("Eb/N0, dB")',
                'plt.ylabel("BER")',
                'plt.plot({}, \'--o\', label=\'QAM-4\')'.format(ber_points_storage_name),
                'plt.legend()',
                'plt.show()'
                ]

    @staticmethod
    def gen_modelling_code(ebn0_max_var: str, ebn0_emitter_block_name: str):
        return NaiveCodeGenerator.gen_for_loop(
            'ebn0 in range({})'.format(ebn0_max_var),
            ['{}.value = ebn0'.format(ebn0_emitter_block_name), ''] + NaiveCodeGenerator.gen_model_traversal()
        )

    @staticmethod
    def gen_model_traversal():
        front_init = ['front = set()']
        front_init += NaiveCodeGenerator.gen_for_loop(
            'b in blocks',
            NaiveCodeGenerator.gen_if_else('b.is_source_block()', ['front.add(b)'], ['pass'])
        )
        front_init += ['']

        front_traversal = NaiveCodeGenerator.gen_for_loop('b in front', [
            'b.execute()',
            'new_front.update(b.get_children())'
        ])

        front_update = NaiveCodeGenerator.gen_if_else(
            'new_front', ['front = new_front'], ['break']
        )

        model_traversal = front_init + NaiveCodeGenerator.gen_while_loop(
            'True',
            ['new_front = set()', *front_traversal, *front_update]
        )
        return model_traversal

    @staticmethod
    def gen_for_loop(condition: str, body: List[str]) -> List[str]:
        lines = ['for {}:'.format(condition)]
        for x in body:
            lines.append('\t{}'.format(x))
        return lines

    @staticmethod
    def gen_while_loop(condition: str, body: List[str]) -> List[str]:
        lines = ['while {}:'.format(condition)]
        for x in body:
            lines.append('\t{}'.format(x))
        return lines

    @staticmethod
    def gen_if_else(condition: str, body1: List[str], body2: List[str]) -> List[str]:
        lines = ['if {}:'.format(condition)]
        for x in body1:
            lines.append('\t{}'.format(x))
        lines.append('else:')
        for x in body2:
            lines.append('\t{}'.format(x))
        return lines

    @staticmethod
    def gen_connection_import():
        return 'from base.connection.connection_implementation import ConnectionImplementation'

    def gen_connection_construction(self, connection: ConnectionSceneItemDraft):
        # ConnectionImplementation(bin_gen.outputs[0], awgn_channel.inputs[0])

        src_port = self.gen_port_addressing(connection.source)
        dst_port = self.gen_port_addressing(connection.destination)

        var_name = self.get_var_name_for_new_connection()
        self.scene_connection_to_var_name[connection] = var_name

        return '{} = ConnectionImplementation({}, {})'.format(var_name, src_port, dst_port)

    def get_var_name_for_new_connection(self):
        base_name = 'c'
        num = 0
        name = base_name + str(num)
        while name in self.scene_connection_to_var_name.values():
            num += 1
            name = base_name + str(num)
        return name

    def gen_port_addressing(self, port: PortSceneItem):
        block_var_name = self.scene_block_to_var_name[port.block]
        if port.port_type == PortType.OUTPUT_PORT:
            return '{}.outputs[{}]'.format(block_var_name, port.number)
        elif port.port_type == PortType.INPUT_PORT:
            return '{}.inputs[{}]'.format(block_var_name, port.number)

    def gen_block_creation2(self, block: BlockSceneItem, block_params: List[Parameter]):
        cls = NaiveCodeGenerator.get_implementation(block)
        block_var_name = self.get_var_name_for_new_block(block)

        str_block_construction = '{}({})'.format(cls.__name__, NaiveCodeGenerator.gen_constructor_params(block_params))

        self.block_var_names.append(block_var_name)
        self.scene_block_to_var_name[block] = block_var_name

        return self.gen_assignment_to_var(block_var_name, str_block_construction)

    def get_var_name_for_new_block(self, block: BlockSceneItem):
        cls = NaiveCodeGenerator.get_implementation(block)
        base_name = cls.__name__.lower()
        num = 0
        name = base_name + str(num)
        while name in self.block_var_names:
            num += 1
            name = base_name + str(num)
        return name

    def gen_assignment_to_var(self, var_name: str, operand: str):
        return '{} = {}'.format(var_name, operand)

    @staticmethod
    def get_implementation(block: BlockSceneItem):
        folder_name = '/'.join(block.__module__.split('.')[:-1])
        return BlockLibLoader.find_implementation_cls(folder_name)

    @staticmethod
    def gen_block_import(block: BlockSceneItem):
        cls = NaiveCodeGenerator.get_implementation(block)
        str_import = 'from {} import {}'.format(cls.__module__, cls.__name__)
        return str_import

    @staticmethod
    def gen_constructor_params(params: List[Parameter]) -> str:
        strings = []
        for f in params:
            # template: field_name=value
            s = '{}={}, '.format(f.name, f.data)
            strings.append(s)
        return ''.join(strings)
