#pragma once
#include <exception>
#include <string>

class AuditException : public std::exception {
private:
    std::string message;
    std::string logFile;

public:
    AuditException(const std::string& file, long count);
    const char* what() const noexcept;
};
