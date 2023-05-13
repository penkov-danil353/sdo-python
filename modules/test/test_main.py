from typing import List, Any, Dict, Tuple, Set

from modules.analize.check_func import *
from modules.models.db_class import *
from .test_run import *
from base64 import decodebytes as bdecode

import pytest


def tonumber(value: str) -> Any:
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def gentest(function: str, data: List[Tuple[Any]], i: str) -> str:
    letters: str = ', '.join([chr(i) for i in range(97, 97 + len(data[0][:-1]))])
    test: str = '''@pytest.mark.parametrize("''' + letters + ', expected_result", ' + data.__str__() + ''')
def test_''' + function + '_' + i + '(' + letters + ''', expected_result):
    assert ''' + function + '(' + letters + ') == expected_result\n\n\n'
    return test


def a(filename: str, function_test: List[Function], unique_id: str) -> None:
    with open(f'./trash/{unique_id}/test_{filename}', 'w') as test:
        test.write('''from '''+filename[:-3]+''' import *
import pytest


''')
        i: int = 0
        for function in function_test:
            set1: Set[str] = set([data.data_pose for data in function.datas])
            datas: List[Any] = [tonumber(data.data) for data in function.datas]
            data_t: List[Tuple[Any]] = [tuple([data for data in datas[i:i+len(set1)]])
                                        for i in range(0, len(datas), len(set1))]
            funcname: str = function.func_name
            test.write(gentest(funcname, data_t, str(i)))
            i = i + 1
    pytest.main(["-q", f'./trash/{unique_id}/test_{filename}', f"--junitxml=./trash/{unique_id}/output.xml"])


def write_file(filename: str, file: str, unique_id: str) -> None:
    with open(f'./trash/{unique_id}/{filename}', 'w') as test_file:
        test_file.write(bdecode(file.encode('utf-8')).decode('utf-8'))


def run_test(filename: str, func: List[Function], unique_id: str) -> Dict[str, List[Any]]:
    a(filename, func, unique_id)
    run(filename, unique_id)
    checks: Dict[str, list] = {}
    for function in func:
        formulas: List[Formula] = list([formula for formula in function.formulas])
        if not checks.get(function.func_name, False) and len(formulas) != 0:
            checks[function.func_name] = []
        if len(formulas) > 1:
            formula_parsed: List[List[str]] = [[]]
            i: int = 0
            last_state: int = 0
            for formula in formulas:
                if last_state > formula.num:
                    i += 1
                    formula_parsed.append([])
                last_state = formula.num
                formula_parsed[i].append(formula.formula)
            for formulas_t in formula_parsed:
                buffer: List[Any] = []
                for formula_t in formulas_t:
                    buffer.append(formula_t)
                if len(formulas_t) > 1:
                    buffer.append(check_multiple_formulas(filename, function.func_name, formulas_t, unique_id))
                elif len(formulas_t) == 1:
                    buffer.append(check_single_formula(filename, function.func_name, formulas_t.pop(), unique_id))
                checks[function.func_name].append(buffer)
        elif len(formulas) == 1:
            formula = formulas.pop().formula
            checks[function.func_name].append([formula, check_single_formula(
                filename, function.func_name, formula, unique_id)])
    return checks


__all__ = ["run_test", "write_file"]
