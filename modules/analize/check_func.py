from parsewrapper import calc_evaluation
from itertools import permutations
from random import random
import re


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
    vars_set.sort()
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


def check(func_lines: list, formula: str) -> bool:
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
            f_val.append(calc_evaluation(replace_vars(formula, value)))
        except Exception:
            pass
    f_val.sort()
    i: int = 0
    file_vals: list = []
    for match in matches:
        file_vals.append([])
        for value in values:
            try:
                file_vals[i].append(calc_evaluation(replace_vars(match, value)))
            except Exception:
                pass
        file_vals[i].sort()
        i += 1
    for file_val in file_vals:
        for i in range(len(values)):
            if f_val[i] == file_val[i]:
                return True
    return False


if __name__ == "__main__":
    lines: list = get_func_lines("compute_binom.py", "compute_binom")
    print(check(lines, "a-b"))
