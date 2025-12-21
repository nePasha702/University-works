#include "Validator.h"

Validator::Validator() 
    : minLength(3), isRequired(true) {}

bool Validator::validateString(std::string value) {
    if (isRequired && value.empty()) {
        lastError = "Поле не может быть пустым";
        return false;
    }
    if (value.length() < minLength) {
        lastError = "Слишком короткое значение";
        return false;
    }
    return true;
}

std::string Validator::getLastError() const {
    return lastError;
}