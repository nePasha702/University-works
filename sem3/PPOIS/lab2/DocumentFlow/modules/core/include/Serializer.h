#pragma once
#include <string>

// Сериализация данных
class Serializer {
private:
    std::string format;     // Формат (JSON/XML)
    bool compress;          // Сжатие данных
    int version;            // Версия формата

public:
    Serializer();
    std::string serialize(std::string data);
};