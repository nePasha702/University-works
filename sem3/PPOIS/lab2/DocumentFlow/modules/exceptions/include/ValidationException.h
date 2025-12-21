#pragma once
#include <exception>
#include <string>

class ValidationException : public std::exception {
private:
    std::string message;

public:
    ValidationException(const std::string& field, const std::string& value);
    const char* what() const noexcept;
};