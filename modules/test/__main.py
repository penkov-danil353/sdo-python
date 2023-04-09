from json import load as jload
from base64 import decodebytes as bdecode
import subprocess


def a():
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
