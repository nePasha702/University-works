#pragma once
#include <exception>
#include <string>

class UserException : public std::exception {
private:
    std::string message;
    std::string userName;

public:
    UserException(const std::string& user, const std::string& role);
    const char* what() const noexcept;
};