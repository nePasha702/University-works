#pragma once
#include <exception>
#include <string>

class DocumentException : public std::exception {
private:
    std::string message;    // Текст ошибки
    int errorCode;          // Код ошибки
    std::string documentId; // ID документа

public:
    DocumentException(const std::string& msg, int code, const std::string& docId);
    const char* what() const noexcept;
    std::string getDocumentId() const;
};