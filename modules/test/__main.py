from modules.models.db_class import *
from .__run import *
from base64 import decodebytes as bdecode
import pytest


def tonumber(value: str):
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def gentest(function: str, data: list, i: str):
    letters = ', '.join([chr(i) for i in range(97, 97 + len(data[0][:-1]))])
    test = '''@pytest.mark.parametrize("''' + letters + ', expected_result", ' + data.__str__() + ''')
def test_''' + function + '_' + i + '(' + letters + ''', expected_result):
    assert ''' + function + '(' + letters + ') == expected_result\n\n\n'
    return test


def a(filename: str, function_test: List[Function]):
    with open('./trash/test_'+filename, 'w') as test:
        test.write('''from '''+filename[:-3]+''' import *
import pytest


''')
        i: int = 0
        for function in function_test:
            set1 = set([data.data_pose for data in function.datas])
            datas = [tonumber(data.data) for data in function.datas]
            data_t = [tuple([data for data in datas[i:i+len(set1)]]) for i in range(0, len(datas), len(set1))]
            funcname = function.func_name
            test.write(gentest(funcname, data_t, str(i)))
            i = i + 1
    pytest.main(["-q", './trash/test_'+filename, "--junitxml=./trash/output.xml"])


def write_file(filename: str, file: str):
    with open('./trash/'+filename, 'w') as test_file:
        test_file.write(bdecode(file.encode('utf-8')).decode('utf-8'))


def run_test(filename: str, func: List[Function]):
    a(filename, func)
    run(filename)


if __name__ == "__main__":
    func = [Function(
        func_name="compute_binom",
        datas=[Data(data_pose=0, data="2"), Data(data_pose=1, data="2"), Data(data_pose=-1, data="1"),
               Data(data_pose=0, data="1"), Data(data_pose=1, data="1"), Data(data_pose=-1, data="1"),
               Data(data_pose=0, data="2"), Data(data_pose=1, data="1"), Data(data_pose=-1, data="2"),
               Data(data_pose=0, data="10"), Data(data_pose=1, data="1"), Data(data_pose=-1, data="10"),
               Data(data_pose=0, data="10"), Data(data_pose=1, data="2"), Data(data_pose=-1, data="45"),
               Data(data_pose=0, data="15"), Data(data_pose=1, data="2"), Data(data_pose=-1, data="105"),
               Data(data_pose=0, data="100"), Data(data_pose=1, data="3"), Data(data_pose=-1, data="161700"),
               Data(data_pose=0, data="64"), Data(data_pose=1, data="7"), Data(data_pose=-1, data="621216192")],
        formulas=[Formula(num=0, formula="z = n - k")]
    ), Function(
        func_name="factorial",
        datas=[Data(data_pose=0, data="0"), Data(data_pose=-1, data="1"),
               Data(data_pose=0, data="1"), Data(data_pose=-1, data="1"),
               Data(data_pose=0, data="2"), Data(data_pose=-1, data="2"),
               Data(data_pose=0, data="3"), Data(data_pose=-1, data="6"),
               Data(data_pose=0, data="4"), Data(data_pose=-1, data="24")],
        formulas=[Formula(num=0, formula="z = n - k")]
    )]
    a("factorial.py", func)
    run("factorial.py")
