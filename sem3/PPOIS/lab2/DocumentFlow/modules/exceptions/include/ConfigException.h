#pragma once
#include <exception>
#include <string>

class ConfigException : public std::exception {
private:
    std::string message;
    std::string configKey;

public:
    ConfigException(const std::string& key, const std::string& expected);
    const char* what() const noexcept;
};