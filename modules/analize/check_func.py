from modules.parse.parsewrapper import calc_evaluation
from itertools import permutations
from random import random
import tokenize
import io
import re


def get_match(formula: str, lines: list) -> list:
    matches: list = []
    formula = formula.replace(" ", "")
    pattern: re.Pattern = re.compile(r'\*\*?|/|\+|-|\(|\)', re.IGNORECASE)
    f_ops: list = re.findall(pattern, formula)
    f_ops.sort()
    for line in lines:
        if re.fullmatch(r'\A.*=[^:]*\Z', line):
            file_ops: list = re.findall(pattern, line)
            file_ops.sort()
            if file_ops == f_ops:
                matches.append(line.replace(" ", "").replace('\n', '').replace('\r', ''))
    return matches


def get_func_lines(filename: str, funcname: str) -> list:
    with open('./trash/'+filename, 'r') as file:
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
        if flag and re.fullmatch(r'\A\s*?def\s*?' + funcname + r'\s*?\(.*?\)\s*?:\s*?\Z', line):
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


def solve_values(values: list, formula: str) -> list:
    val: list = []
    for value in values:
        try:
            val.append(calc_evaluation(replace_vars(formula, value)))
        except Exception:
            pass
    val.sort()
    return val


def check_single(func_lines: list, formula: str) -> bool:
    matches: list = [line[line.rfind('=') + 1:] for line in get_match(formula, func_lines)]
    values: list = gen_values(get_vars(formula))
    f_val: list = solve_values(values, formula)
    file_vals: list = []
    for match in matches:
        file_vals.append(solve_values(values, match))
    for file_val in file_vals:
        if file_val == f_val:
            return True
    return False


def check_single_formula(filename: str, func_name: str, formula: str) -> bool:
    return check_single(get_func_lines(filename, func_name), formula)


def get_tokens(formulas: list) -> list:
    tokens_list: list = []
    for i in range(0, len(formulas)):
        try:
            tokens_list.append([token for token in tokenize.generate_tokens(io.StringIO(formulas[i]).readline)])
        except tokenize.TokenError as tkE:
            print(tkE.__str__())
    return tokens_list


def tokens_match(tokens: list) -> list:
    tokens_in_1: list = []
    for token in tokens[1]:
        if token.type == 1:
            for token1 in tokens[0]:
                if token1.type == 1 and token1.string == token.string:
                    tokens_in_1.append(tokens[0].index(token1))
    tokens_in_1.sort()
    return tokens_in_1


def check_multiple(func_lines: list, formulas: list) -> bool:
    tokens_list: list = get_tokens(formulas)
    tokens_in_1: list = tokens_match(tokens_list)
    matches: list = [get_match(formulas[0], func_lines), get_match(formulas[1], func_lines)]
    for match1 in matches[0]:
        for match2 in matches[1]:
            if tokens_in_1 == tokens_match(get_tokens([match1, match2])):
                return True
    return False


def check_multiple_formulas(filename: str, func_name: str, formulas: list) -> bool:
    return check_multiple(get_func_lines(filename, func_name), formulas)
