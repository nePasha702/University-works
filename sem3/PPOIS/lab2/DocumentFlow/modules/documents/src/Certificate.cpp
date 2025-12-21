#include "Certificate.h"
#include <ctime>

Certificate::Certificate(std::string id, std::string owner, std::string certType)
    : DocumentBase(id), holder(owner), type(certType) {
    issueDate = time(nullptr);
}

bool Certificate::validate() {
    return !holder.empty() && !type.empty();
}

std::string Certificate::generateReport() {
    return "Сертификат #" + id + " для " + holder + " (" + type + ")";
}

bool Certificate::isExpired() {
    // Истекает через 1 год
    return time(nullptr) - issueDate > 365 * 24 * 3600;
}