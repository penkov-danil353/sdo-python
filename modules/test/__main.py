from modules.models.db_class import *
from .__run import *
from base64 import decodebytes as bdecode
from modules.analize.check_func import *
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


def run_test(filename: str, func: List[Function]) -> Dict[str, list]:
    a(filename, func)
    run(filename)
    checks: Dict[str, list] = {}
    for function in func:
        formulas = list([formula for formula in function.formulas])
        if not checks.get(function.func_name, False) and len(formulas) != 0:
            checks[function.func_name] = []
        if len(formulas) > 1:
            formula_parsed: List[list] = [[]]
            i: int = 0
            last_state: int = 0
            for formula in formulas:
                if last_state > formula.num:
                    i += 1
                    formula_parsed.append([])
                last_state = formula.num
                formula_parsed[i].append(formula.formula)
            for formulas_t in formula_parsed:
                buffer: list = []
                for formula_t in formulas_t:
                    buffer.append(formula_t)
                if len(formulas_t) > 1:
                    buffer.append(check_multiple_formulas(filename, function.func_name, formulas_t))
                elif len(formulas_t) == 1:
                    buffer.append(check_single_formula(filename, function.func_name, formulas_t.pop()))
                checks[function.func_name].append(buffer)
        elif len(formulas) == 1:
            formula = formulas.pop().formula
            checks[function.func_name].append([formula, check_single_formula(filename, function.func_name, formula)])
    return checks
