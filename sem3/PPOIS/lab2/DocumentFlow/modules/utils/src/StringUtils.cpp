#include "StringUtils.h"
#include <algorithm>
#include <cctype>

std::string StringUtils::toUpperCase(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
        [](unsigned char c) { return std::toupper(c); });
    return result;
}

std::string StringUtils::trim(const std::string& str) {
    size_t start = str.find_first_not_of(" ");
    size_t end = str.find_last_not_of(" ");
    return (start == std::string::npos || end == std::string::npos) ? "" : str.substr(start, end - start + 1);
}