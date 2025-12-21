#include "StorageException.h"

StorageException::StorageException(const std::string& path, long long space)
    : storagePath(path) {
    message = "Ошибка хранилища: " + path + ". Свободно: " + std::to_string(space) + " байт";
}

const char* StorageException::what() const noexcept {
    return message.c_str();
}