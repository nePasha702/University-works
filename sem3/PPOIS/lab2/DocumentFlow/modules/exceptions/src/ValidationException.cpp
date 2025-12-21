#include "ValidationException.h"

ValidationException::ValidationException(const std::string& field, const std::string& value)
    : message("Ошибка валидации поля " + field + ": " + value) {}

const char* ValidationException::what() const noexcept {
    return message.c_str();
}