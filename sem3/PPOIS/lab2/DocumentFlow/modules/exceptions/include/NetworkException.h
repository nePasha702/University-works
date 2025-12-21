#pragma once
#include <exception>
#include <string>

class NetworkException : public std::exception {
private:
    std::string message;
    std::string serverAddress;

public:
    NetworkException(const std::string& address, int port);
    const char* what() const noexcept;
};