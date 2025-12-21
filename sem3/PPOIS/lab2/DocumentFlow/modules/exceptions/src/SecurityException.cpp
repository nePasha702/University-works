#include "SecurityException.h"

SecurityException::SecurityException(const std::string& user, const std::string& act)
    : userId(user), action(act) {
    message = "Доступ запрещён для " + user + " при попытке " + act;
}

const char* SecurityException::what() const noexcept {
    return message.c_str();
}