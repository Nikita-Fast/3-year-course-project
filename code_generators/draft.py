from typing import List

from utils.parameter import Parameter


class NaiveCodeGenerator:

    @staticmethod
    def gen_constructor_params(params: List[Parameter]) -> str:
        code = ''
        strings = []
        for f in params:
            # template: field_name=value
            s = '{0}={1}, '.format(f.name, f.data)
            strings.append(s)
        return ''.join(strings)

    @staticmethod
    def gen_obj_construction(obj_type: type, params: List[Parameter]):
        str_params = NaiveCodeGenerator.gen_constructor_params(params)
        return '{}({})'.format(obj_type.__name__, str_params)
