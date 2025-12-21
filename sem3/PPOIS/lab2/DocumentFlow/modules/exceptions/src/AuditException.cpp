#include "AuditException.h"

AuditException::AuditException(const std::string& file, long count)
    : logFile(file) {
    message = "Ошибка аудита: " + file + ". Записей: " + std::to_string(count);
}

const char* AuditException::what() const noexcept {
    return message.c_str();
}
