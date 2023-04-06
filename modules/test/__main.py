from json import load as jload
from base64 import decodebytes as bdecode
import subprocess

with open('test_data.json', 'r') as json_file:
    json_data = jload(json_file)

with open(json_data['test_file_name'], 'w') as test_file:
    test_file.write(bdecode(json_data['test_file'].encode('utf-8')).decode('utf-8'))

letters = ', '.join([chr(i) for i in range(97, 97+int(json_data['test_data_var_count']))])

with open('test_'+json_data['test_file_name'], 'w') as test:
    test.write('''
from '''+json_data['test_file_name'][:-3]+''' import '''+json_data['test_func_name']+'''
import pytest

pytest.main(['--junitxml=output.xml'])

@pytest.mark.parametrize("'''+letters+''', expected_result", '''+json_data['test_data']+''')
def test_'''+json_data['test_func_name']+'''_test_1('''+letters+''', expected_result):
    assert '''+json_data['test_func_name']+'''('''+letters+''') == expected_result

def run():
    pytest.main()
''')

with open('__run.py', 'w') as run:
    run.write('''
import check_func
import os
import re
import subprocess
import test_'''+json_data['test_file_name'][:-3]+'''


def gen_config():
    os.system('pylint --generate-rcfile > .pylintrc')


def clear_output(check_result):
    rows = check_result.split('\\n')
    struct_result = dict()
    cur_module = ""
    for row in rows:
        if cur_module != "" and re.match(cur_module + r'\.py', row) is not None:
            # error_name = re.search(r'\(.*\)', row).group(0)[1:-1]
            error_name = row[row.rfind('(') + 1:-1]
            if struct_result[cur_module].get(error_name) is None:
                struct_result[cur_module][error_name] = list()
            struct_result[cur_module][error_name].append('line' + row[len(cur_module) + 3:-(len(error_name) + 3)])
        elif re.match(r'[*]{13} .* .*', row) is not None:
            cur_module = row.split(' ')[-1]
            struct_result[cur_module] = dict()
    #del struct_result['text']
    return struct_result


if __name__ == "__main__":
    filename = "'''+json_data['test_file_name']+'''"
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
    test_'''+json_data['test_file_name'][:-3]+'''.run()
    print(check_func.check(check_func.get_func_lines("'''+json_data['test_file_name']+'''", "'''+json_data['test_func_name']+'''"), "''' + json_data['test_formula']+'''"))
''')
