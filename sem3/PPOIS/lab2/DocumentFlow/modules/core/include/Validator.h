#pragma once
#include <string>

// Валидация данных
class Validator {
private:
    std::string lastError;  // Последняя ошибка
    int minLength;          // Минимальная длина
    bool isRequired;        // Обязательное поле

public:
    Validator();
    bool validateString(std::string value);
    std::string getLastError() const;
};