#include "UserException.h"

UserException::UserException(const std::string& user, const std::string& role)
    : userName(user) {
    message = "Ошибка пользователя: " + user + " (роль: " + role + ")";
}

const char* UserException::what() const noexcept {
    return message.c_str();
}