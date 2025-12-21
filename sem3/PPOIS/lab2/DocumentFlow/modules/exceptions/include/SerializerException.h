#pragma once
#include <exception>
#include <string>

class SerializerException : public std::exception {
private:
    std::string message;
    std::string format;

public:
    SerializerException(const std::string& fmt, const std::string& type);
    const char* what() const noexcept;
};