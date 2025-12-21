#include "DateUtils.h"
#include <ctime>
#include <iomanip>
#include <sstream>

std::string DateUtils::getCurrentDate() {
    auto now = std::time(nullptr);
    std::tm* tm = std::localtime(&now);
    std::ostringstream oss;
    oss << std::put_time(tm, "%Y-%m-%d");
    return oss.str();
}

bool DateUtils::isValidDate(const std::string& date) {
    if (date.length() != 10) return false;
    if (date[4] != '-' || date[7] != '-') return false;
    for (int i = 0; i < 10; i++) {
        if (i == 4 || i == 7) continue;
        if (!isdigit(date[i])) return false;
    }
    return true;
}
