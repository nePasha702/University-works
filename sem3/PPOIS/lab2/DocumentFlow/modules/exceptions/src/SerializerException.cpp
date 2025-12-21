#include "SerializerException.h"

SerializerException::SerializerException(const std::string& fmt, const std::string& type)
    : format(fmt) {
    message = "Ошибка сериализации в формате " + fmt + " для типа " + type;
}

const char* SerializerException::what() const noexcept {
    return message.c_str();
}