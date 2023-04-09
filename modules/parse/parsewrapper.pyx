cdef extern from "library.h":
    double calc_eval(char* str1)

def calc_evaluation(evaluation: str) -> float:
    evaluation = evaluation.replace("**", "^")
    return calc_eval(evaluation.encode('utf-8'))
