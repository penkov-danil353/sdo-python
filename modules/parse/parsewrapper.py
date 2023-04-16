import ctypes
import platform


def calc_evaluation(evaluation: str) -> float:
    evaluation = evaluation.replace("**", "^")
    if platform.system() == "Windows":
        lib = ctypes.CDLL("./libparse.dll")
    else:
        lib = ctypes.CDLL("./libparse.so")
    lib.calc_eval.argtypes = [ctypes.c_char_p, ]
    lib.calc_eval.restype = ctypes.c_double
    return lib.calc_eval(ctypes.c_char_p(evaluation.encode('utf-8')))


if __name__ == "__main__":
    print(calc_evaluation("2*2+2/(2**2)"))
