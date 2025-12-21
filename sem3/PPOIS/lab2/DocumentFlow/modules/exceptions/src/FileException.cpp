#include "FileException.h"

FileException::FileException(const std::string& path, long size)
    : filePath(path) {
    message = "Ошибка файла: " + path + " (размер: " + std::to_string(size) + " байт)";
}

const char* FileException::what() const noexcept {
    return message.c_str();
}