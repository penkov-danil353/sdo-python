import ctypes
import platform


def calc_evaluation(evaluation: str) -> float:
    evaluation = evaluation.replace("**", "^")
    if platform.system() == "Windows":
        lib = ctypes.CDLL("./libparse.dll")
    else:
        try:
            lib = ctypes.CDLL("libparse.so")
        except:
            import os
            lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libparse.so"))
    lib.calc_eval.argtypes = [ctypes.c_char_p, ]
    lib.calc_eval.restype = ctypes.c_double
    return lib.calc_eval(ctypes.c_char_p(evaluation.encode('utf-8')))


__all__ = ["calc_evaluation"]
