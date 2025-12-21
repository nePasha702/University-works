#pragma once
#include <exception>
#include <string>

class WorkflowException : public std::exception {
private:
    std::string message;
    std::string processName;

public:
    WorkflowException(const std::string& process, int step);
    const char* what() const noexcept;
};