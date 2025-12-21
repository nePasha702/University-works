#include "DocumentException.h"

DocumentException::DocumentException(const std::string& msg, int code, const std::string& docId)
    : message(msg), errorCode(code), documentId(docId) {}

const char* DocumentException::what() const noexcept {
    return message.c_str(); 
}

std::string DocumentException::getDocumentId() const {
    return documentId;
}