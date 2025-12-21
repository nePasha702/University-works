#pragma once
#include <string>

class DateUtils {
public:
    static std::string getCurrentDate();     
    static bool isValidDate(const std::string& date); 
};
