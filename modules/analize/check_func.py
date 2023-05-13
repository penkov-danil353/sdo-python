from typing import List, Tuple

from modules.parse.parsewrapper import calc_evaluation
from itertools import permutations
from random import random
import tokenize
import io
import re


def get_match(formula: str, lines: List[str]) -> List[str]:
    matches: List[str] = []
    formula = formula.replace(" ", "")
    pattern: re.Pattern = re.compile(r'\*\*?|/|\+|-|\(|\)', re.IGNORECASE)
    f_ops: List[str] = re.findall(pattern, formula)
    f_ops.sort()
    for line in lines:
        if re.fullmatch(r'\A.*=[^:]*\Z', line):
            file_ops: List[str] = re.findall(pattern, line)
            file_ops.sort()
            if file_ops == f_ops:
                matches.append(line.replace(" ", "").replace('\n', '').replace('\r', ''))
    return matches


def get_func_lines(filename: str, funcname: str, unique_id: str) -> List[str]:
    with open(f'./trash/{unique_id}/{filename}', 'r') as file:
        file_lines: List[str] = file.readlines()
    func: List[str] = []
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


def get_vars(evaluation: str) -> List[str]:
    variables: List[str] = re.split(r'[-+*/()]\*?', evaluation)
    vars_set: List[str] = list(set([var for var in variables if var not in "01234567890."]))
    return [i for i in vars_set if i != '' and i != ' ']


def gen_values(vars_set: List[str]) -> List[Tuple[float]]:
    return list(permutations([random() for _ in range(len(vars_set))]))


def replace_vars(evaluation: str, values: Tuple[float]) -> str:
    vars_set: List[str] = get_vars(evaluation)
    if len(vars_set) == len(values):
        pairs = dict(zip(vars_set, values))
        for key, val in pairs.items():
            evaluation = evaluation.replace(key, str(val))
        return evaluation
    else:
        raise ValueError("1")


def solve_values(values: List[Tuple[float]], formula: str) -> List[float]:
    val: List[float] = []
    for value in values:
        try:
            val.append(calc_evaluation(replace_vars(formula, value)))
        except Exception:
            pass
    val.sort()
    return val


def check_single(func_lines: list, formula: str) -> bool:
    matches: List[str] = [line[line.rfind('=') + 1:] for line in get_match(formula, func_lines)]
    values: List[Tuple[float]] = gen_values(get_vars(formula))
    f_val: List[float] = solve_values(values, formula)
    file_vals: List[List[float]] = []
    for match in matches:
        file_vals.append(solve_values(values, match))
    for file_val in file_vals:
        if file_val == f_val:
            return True
    return False


def check_single_formula(filename: str, func_name: str, formula: str, unique_id: str) -> bool:
    return check_single(get_func_lines(filename, func_name, unique_id), formula)


def get_tokens(formulas: List[str]) -> List[List[tokenize.TokenInfo]]:
    tokens_list: List[List[tokenize.TokenInfo]] = []
    for i in range(0, len(formulas)):
        try:
            tokens_list.append([token for token in tokenize.generate_tokens(io.StringIO(formulas[i]).readline)])
        except tokenize.TokenError as tkE:
            print(tkE.__str__())
    return tokens_list


def tokens_match(tokens: List[List[tokenize.TokenInfo]]) -> List[int]:
    tokens_in_1: List[int] = []
    for token in tokens[1]:
        if token.type == 1:
            for token1 in tokens[0]:
                if token1.type == 1 and token1.string == token.string:
                    tokens_in_1.append(tokens[0].index(token1))
    tokens_in_1.sort()
    return tokens_in_1


def check_multiple(func_lines: List[str], formulas: List[str]) -> bool:
    tokens_list: List[List[tokenize.TokenInfo]] = get_tokens(formulas)
    tokens_in_1: List[int] = tokens_match(tokens_list)
    matches: List[List[str]] = [get_match(formulas[0], func_lines), get_match(formulas[1], func_lines)]
    for match1 in matches[0]:
        for match2 in matches[1]:
            if tokens_in_1 == tokens_match(get_tokens([match1, match2])):
                return True
    return False


def check_multiple_formulas(filename: str, func_name: str, formulas: List[str], unique_id: str) -> bool:
    return check_multiple(get_func_lines(filename, func_name, unique_id), formulas)


__all__ = ["check_multiple_formulas", "check_single_formula"]
