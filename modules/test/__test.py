from types import ModuleType
import sys
import pytest
import importlib
import importlib.util


def decorate(func: str, params: list, data: list):
    #__dict__[func] = getattr(ModuleType, func)
    calc = '''import pytest
@pytest.mark.parametrize("'''+', '.join(params)+'", '+data.__str__()+''')
def test_'''+func+'('+', '.join(params)+'''):
    assert module.'''+func+'('+', '.join(params[:-1])+') == ' + params[-1]
    exec(calc, globals())


def run(file_name: str, func_name: str, params: list, data: list):
    if file_name in sys.modules:
        print(f"{file_name!r} already in sys.modules")
    elif (spec := importlib.util.find_spec(file_name)) is not None:
        # Если надо выполнить фактический импорт ...
        module = importlib.util.module_from_spec(spec)
        sys.modules[file_name] = module
        spec.loader.exec_module(module)
        print(f"{file_name!r} has been imported")
    else:
        print(f"can't find the {file_name!r} module")
    print(dir(sys.modules[file_name]))
    decorate(func_name, params, data)


if __name__ == "__main__":
    run("factorial", "compute_binom", ["a", "b", "expected_result"], [(1, 1, 1), (2, 1, 2), (10, 1, 10), (10, 2, 45), (15, 2, 105), (100, 3, 161700), (64, 7, 621216192)])
