#ifndef PARSE_LIBRARY_H
#define PARSE_LIBRARY_H
#define _USE_MATH_DEFINES

#include <algorithm>
#include <iostream>
#include <vector>
#include <cmath>
#include <cstring>
#include <cstdlib>

#ifdef __cplusplus
extern "C"
{
#endif

__declspec (dllexport) double calc_eval(char* eval);

#ifdef __cplusplus
}
#endif

#endif //PARSE_LIBRARY_H
