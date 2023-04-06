#ifndef PARSE_LIBRARY_H
#define PARSE_LIBRARY_H
#define _USE_MATH_DEFINES

#include <algorithm>
#include <iostream>
#include <vector>
#include <cmath>
#include <cstring>
#include <cstdlib>

bool check_brackets(const char* eval);
bool isUnary(const char* eval, const size_t& op_pos);
bool check_op_in_br(const char* eval, const size_t& op_pos);
int find_op_w(const char& op);
bool symb_is_num(const char& symb);
void check_num(const char* eval);
void check_dots(const char* eval);
int find_rb(const char* eval);
double parse(char* eval);
double calc_eval(char* eval);

#endif //PARSE_LIBRARY_H
