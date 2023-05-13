from typing import Dict, List
import os
import re
import subprocess


def gen_config() -> None:
    os.system('pylint --generate-rcfile > .pylintrc')


def clear_output(check_result: str) -> Dict[str, Dict[str, List[str]]]:
    rows: List[str] = check_result.split('\n')
    struct_result: Dict[str, Dict[str, List[str]]] = dict()
    cur_module = ""
    for row in rows:
        if cur_module != "" and re.match(r'.*/'+cur_module + r'\.py', row) is not None:
            error_name: str = row[row.rfind('(') + 1:-1]
            if struct_result[cur_module].get(error_name) is None:
                struct_result[cur_module][error_name] = list()
            struct_result[cur_module][error_name].append('line' + row[len(cur_module) + 3:-(len(error_name) + 3)])
        elif re.match(r'[*]{13} .* .*', row) is not None:
            cur_module: str = row.split(' ')[-1]
            struct_result[cur_module] = dict()
    return struct_result


def run(filename: str, unique_id: str) -> None:
    status = subprocess.getstatusoutput(f"pylint --reports=y ./trash/{unique_id}/{filename}")
    r = ""
    if status[0] != 127:
        r = clear_output(status[1])
    with open(f'./trash/{unique_id}/errors.txt', 'w') as file:
        for module, errors in r.items():
            file.write(module + '.py:\n')
            for error_name, error_messages in errors.items():
                file.write('\t' + error_name + ':\n')
                for error_message in error_messages:
                    file.write('\t\t' + error_message + '\n')


__all__ = ["run"]
