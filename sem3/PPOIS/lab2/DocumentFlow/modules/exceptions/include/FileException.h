#pragma once
#include <exception>
#include <string>

class FileException : public std::exception {
private:
    std::string message;
    std::string filePath;

public:
    FileException(const std::string& path, long size);
    const char* what() const noexcept;
};