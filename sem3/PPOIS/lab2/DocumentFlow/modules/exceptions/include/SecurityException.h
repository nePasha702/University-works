#pragma once
#include <exception>
#include <string>

class SecurityException : public std::exception {
private:
    std::string message; // Формируемое сообщение
    std::string userId;
    std::string action;

public:
    SecurityException(const std::string& user, const std::string& act);
    const char* what() const noexcept;
};