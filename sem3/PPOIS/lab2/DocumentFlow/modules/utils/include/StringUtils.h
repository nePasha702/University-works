#pragma once
#include <string>

class StringUtils {
public:
    static std::string toUpperCase(const std::string& str); // В верхний регистр
    static std::string trim(const std::string& str);        // Убрать пробелы по краям
};