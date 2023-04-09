from typing import List
from itertools import permutations
from random import random
import tokenize
import io
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "parse"))
a = sys.path[-1]
print(sys.path)
import parsewrapper as pswr


def get_func_lines(filename: str, funcname: str) -> list:
    with open(filename, 'r') as file:
        file_lines: list = file.readlines()
    func: list = []
    flag: bool = True
    findent: str = ""
    for line in file_lines:
        indent = [line[:match.end()] for match in re.finditer(r"\A\s*", line)][0]
        if not flag and len(findent) < len(indent):
            func.append(line)
        elif len(findent) >= len(indent):
            flag = True
        if flag and re.fullmatch(r'\A\s*?def\s*?'+funcname+r'\s*?\(.*?\)\s*?:\s*?\Z', line):
            flag = False
            findent = indent
    return func


def get_vars(evaluation: str) -> list:
    variables = re.split(r'[-+*/()]\*?', evaluation)
    vars_set = list(set([var for var in variables if var not in "01234567890."]))
    return [i for i in vars_set if i != '' and i != ' ']


def gen_values(vars_set: list) -> list:
    return list(permutations([random() for _ in range(len(vars_set))]))


def replace_vars(evaluation: str, values: list) -> str:
    vars_set = get_vars(evaluation)
    if len(vars_set) == len(values):
        pairs = dict(zip(vars_set, values))
        for key, val in pairs.items():
            evaluation = evaluation.replace(key, str(val))
        return evaluation
    else:
        raise ValueError("1")


def check_single(func_lines: list, formula: str) -> bool:
    matches: list = []
    formula = formula.replace(" ", "")
    pattern: re.Pattern = re.compile(r'\*\*?|/|\+|-|\(|\)', re.IGNORECASE)
    f_ops: list = re.findall(pattern, formula)
    f_ops.sort()
    for line in func_lines:
        if re.fullmatch(r'\A.*=[^:]*\Z', line):
            line = line[line.rfind('=')+1:]
            file_ops: list = re.findall(pattern, line)
            file_ops.sort()
            if file_ops == f_ops:
                matches.append(line.replace(" ", "").replace('\n', '').replace('\r', ''))
    f_val: list = []
    values: list = gen_values(get_vars(formula))
    for value in values:
        try:
            f_val.append(pswr.calc_evaluation(replace_vars(formula, value)))
        except Exception:
            pass
    f_val.sort()
    i: int = 0
    file_vals: list = []
    for match in matches:
        file_vals.append([])
        for value in values:
            try:
                file_vals[i].append(pswr.calc_evaluation(replace_vars(match, value)))
            except Exception:
                pass
        file_vals[i].sort()
        i += 1
    for file_val in file_vals:
        if file_val == f_val:
            return True
    return False


def check_single_formula(filename: str, func_name: str, formula: str) -> bool:
    return check_single(get_func_lines(filename, func_name), formula)


def check_multiple(func_lines: List[str], formulas: List[str]) -> bool:
    tokens: list = []
    for i in range(0, len(formulas)):
        tokens.append(list())
        try:
            tokens[i].append(tokenize(io.StringIO(formulas[i]).readline))
            for toknum in tokens[i]:
                print(toknum)
        except tokenize.TokenError as tkE:
            print(tkE.__str__())
    pass


def check_multiple_formulas(filename: str, func_name: str, formulas: List[str]) -> bool:

    pass


if __name__ == "__main__":
    check_multiple(["",], ["s=a+b\n", "d=s*b\n"])
