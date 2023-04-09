from typing import Dict, List

from ..analize.check_func import check_single_formula
import os
import re
import subprocess
#import test_'''+json_data['test_file_name'][:-3]+'''


def gen_config():
    os.system('pylint --generate-rcfile > .pylintrc')


def clear_output(check_result):
    rows = check_result.split('\\n')
    struct_result = dict()
    cur_module = ""
    for row in rows:
        if cur_module != "" and re.match(cur_module + r'\.py', row) is not None:
            error_name = row[row.rfind('(') + 1:-1]
            if struct_result[cur_module].get(error_name) is None:
                struct_result[cur_module][error_name] = list()
            struct_result[cur_module][error_name].append('line' + row[len(cur_module) + 3:-(len(error_name) + 3)])
        elif re.match(r'[*]{13} .* .*', row) is not None:
            cur_module = row.split(' ')[-1]
            struct_result[cur_module] = dict()
    return struct_result


def run(filename: str, func_and_formula: Dict[str, List[str]]) -> bool:
    result = True
    status = subprocess.getstatusoutput("pylint --reports=y text " + filename)
    r = ""
    if status[0] != 127:
        r = clear_output(status[1])
    with open('errors.txt', 'w') as file:
        for module, errors in r.items():
            file.write(module + '.py:\\n')
            for error_name, error_messages in errors.items():
                file.write('\\t' + error_name + ':\\n')
                for error_message in error_messages:
                    file.write('\\t\\t' + error_message + '\\n')
    for func, formula in func_and_formula.items():
        if len(formula) == 1:
            result = result and check_single_formula(filename, func, formula[0])
        else:
            pass
    return result
