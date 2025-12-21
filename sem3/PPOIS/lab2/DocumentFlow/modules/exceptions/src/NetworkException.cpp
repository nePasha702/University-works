#include "NetworkException.h"

NetworkException::NetworkException(const std::string& address, int port)
    : serverAddress(address) {
    message = "Сетевая ошибка к " + address + ":" + std::to_string(port);
}

const char* NetworkException::what() const noexcept {
    return message.c_str();
}