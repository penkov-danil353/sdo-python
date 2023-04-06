#define _USE_MATH_DEFINES

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <regex>
#include <cstring>
#include <cstdlib>
#include "library.h"

//определяет, все ли открытые скобки закрыты
bool check_brackets(const char* eval){
    int br_counter = 0;
    for (int i = 0; i < strlen(eval);i++){
    //for (char letter : eval){
        if (eval[i] == '(') br_counter++;
        else if (eval[i] == ')'){
            br_counter--;
            if (br_counter < 0) break;
        }
    }
    if (br_counter != 0) return false;
    else return true;
}

bool isUnary(const char* eval, const size_t& op_pos){
    char repl[] = " ";
    if (op_pos > 0) repl[0] = eval[op_pos-1];
    if (eval[op_pos]=='-' && op_pos == 0) return true;
    else if (eval[op_pos]=='-' && strstr("0123456789.)", repl) == nullptr) return true;
    else return false;
}

bool check_op_in_br(const char* eval, const size_t& op_pos){
    std::vector<int> lb_poses;
    std::vector<std::pair<int,int>> br_poses;
    if (eval[op_pos]=='(' || eval[op_pos]==')') return false;
    for(int i = 0; i < strlen(eval); i++){
        if (eval[i] == '('){
            lb_poses.push_back(i);
            br_poses.push_back({i, -1});
        }
        if (eval[i]==')'){
            auto it = std::find(br_poses.begin(), br_poses.end(),
                                std::pair<int,int>(lb_poses.back(), -1));
            it->second = i;
            lb_poses.pop_back();
        }
    }
    for (auto br: br_poses){
        if (op_pos > br.first && op_pos < br.second) return true;
    }
    return false;
}

//определяет вес оператора
int find_op_w(const char& op){
    int weight;
    switch (op) {
        case ')':
            weight = -2;
            break;
        case '(':
            weight = 0;
            break;
        case '^':
            weight = 2;
            break;
        case '*': case '/':
            weight = 3;
            break;
        case '+': case '-':
            weight = 4;
            break;
        default:
            weight = -1;
            break;
    }
    return weight;
}

//определяет является ли числом символ
bool symb_is_num(const char& symb){
    return symb >= '0' && symb <= '9';
}

//определяет, является ли строка правильно записанным числом
void check_num(const char* eval){
    for (int i = 0; i < strlen(eval); i++){
        if (!(symb_is_num(eval[i]) || eval[i] == '.'))
            throw std::invalid_argument("Введенный параметр не является числом");
    }
}

//проверяет, одна ли точка в записи числа
void check_dots(const char* eval){
    bool delimiter = false;
    if (eval[0]=='.') throw std::runtime_error("Ошибка в записи числа");
    for (int i = 1; i < strlen(eval); i++){
        if (eval[i] == '.' && symb_is_num(eval[i-1])){
            if (delimiter) throw std::runtime_error("Ошибка в записи числа");
            delimiter = true;
        }
    }
}

int find_rb(const char* eval){
    for (int i = strlen(eval); i >= 0; i--){
        if (eval[i] == ')') return i;
    }
    return -1;
}

//рекурсивно проводит вычисление функции путем поиска оператора с наименьшим приоритетом
//однако есть исключения:
//если в строке первый символ -, то он распознается как часть числа
//если открывающая скобка встречается раньше, чем другие операторы, то меняет приоритет на нее
double parse(char* eval){
    double ans;
    char *evall = nullptr, *evalr = nullptr;
    int prior[3] = {-1, -1, -1};
    int weight = -3;
    if (!check_brackets(eval)) throw std::runtime_error("Неправильно расставлены скобки");
    for (int i = 0; i < strlen(eval); i++){
        weight = isUnary(eval,i) ? 1 : find_op_w(eval[i]);
        if (weight > prior[1] && !check_op_in_br(eval, i)) {
            prior[0] = i;
            prior[1] = weight;
            prior[2] = (unsigned char)eval[i];
        }
    }
    switch(prior[1]){
    case 2:case 3: case 4:
            eval[prior[0]] = '\0';
            evall = new char[strlen(eval)+1];
            evalr = new char[strlen(eval+prior[0]+1)];
            memcpy(evall, eval, strlen(eval)+1);
            memcpy(evalr, eval+1+prior[0], strlen(eval+prior[0]+1));
            evall[strlen(eval)]='\0';
            evalr[strlen(eval+prior[0]+1)]='\0';
        break;
        case 0:
            eval[find_rb(eval)] = '\0';
            evall = new char[strlen(eval)];
            memcpy(evall, eval+1, strlen(eval));
            evall[strlen(eval)-1]='\0';
            break;
        case 1:
            evall = new char[strlen(eval)];
            memcpy(evall, eval+1, strlen(eval));
            eval[strlen(eval)-1]='\0';
            break;
    }
    switch (prior[1]) {
        case 4:
            if (prior[2]=='+') {
                ans = parse(evall) + parse(evalr);
            }
            if (prior[2]=='-'){
                ans = parse(evall) - parse(evalr);
            }
            break;
        case 3:
            if (prior[2]=='*'){
                ans = parse(evall) * parse(evalr);
            }
            if (prior[2]=='/') {
                ans = parse(evall) / parse(evalr);
            }
            break;
        case 2:
            ans = pow(parse(evall), parse(evalr));
            break;
        case 0:
            ans = parse(evall);
            break;
        case 1:
            ans = -parse(evall);
            break;
        case -1:
            check_dots(eval);
            check_num(eval);
            ans = std::stod(eval);
            break;
    }
    delete[] evall;
    delete[] evalr;
    return ans;
}

double calc_eval(char* eval){
    return parse(eval);
}
