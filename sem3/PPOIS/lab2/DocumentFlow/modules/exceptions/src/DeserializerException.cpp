#include "DeserializerException.h"

DeserializerException::DeserializerException(const std::string& src, int lineNumber)
    : source(src) {
    message = "Ошибка десериализации в " + src + " на строке " + std::to_string(lineNumber);
}

const char* DeserializerException::what() const noexcept {
    return message.c_str();
}