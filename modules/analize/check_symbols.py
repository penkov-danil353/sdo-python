from typing import List, Dict

from modules.models.db_class import CodeLength

import re


def check_symbols(filename: str, lengths: CodeLength, unique_id: str) -> Dict[str, int | bool | None]:
    with open(f'./trash/{unique_id}/{filename}', 'r') as file:
        lines: List[str] = file.readlines()
    symbols: int = 0
    lines_count: int = 0
    for line in lines:
        symbols += len(re.sub(r'\s', '', line))
        lines_count += 1
    result: Dict[str, int | bool | None] = dict.fromkeys(["TaskSymbols", "TaskRows", "UserSymbols",
                                                          "UserRows", "Symbols", "Rows"])
    result["TaskSymbols"] = lengths.symbols
    result["TaskRows"] = lengths.rows
    result["UserSymbols"] = symbols
    result["UserRows"] = lines_count
    result["Symbols"] = lengths.symbols > symbols
    result["Rows"] = lengths.rows > lines_count
    return result


__all__ = ["check_symbols"]
