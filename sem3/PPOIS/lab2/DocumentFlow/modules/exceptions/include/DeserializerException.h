#pragma once
#include <exception>
#include <string>

class DeserializerException : public std::exception {
private:
    std::string message;
    std::string source;

public:
    DeserializerException(const std::string& src, int lineNumber);
    const char* what() const noexcept;
};