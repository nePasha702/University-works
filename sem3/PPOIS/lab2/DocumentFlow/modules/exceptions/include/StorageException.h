#pragma once
#include <exception>
#include <string>

class StorageException : public std::exception {
private:
    std::string message;
    std::string storagePath;

public:
    StorageException(const std::string& path, long long space);
    const char* what() const noexcept;
};