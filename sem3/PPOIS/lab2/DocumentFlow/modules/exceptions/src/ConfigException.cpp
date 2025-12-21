#include "ConfigException.h"

ConfigException::ConfigException(const std::string& key, const std::string& expected)
    : configKey(key) {
    message = "Ошибка конфигурации для ключа " + key + ". Ожидалось: " + expected;
}

const char* ConfigException::what() const noexcept {
    return message.c_str();
}