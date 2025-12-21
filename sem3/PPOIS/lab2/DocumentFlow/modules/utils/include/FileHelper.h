#pragma once
#include <string>
#include <vector>

class FileHelper {
public:
    static bool fileExists(const std::string& path); // Проверка существования файла
    static std::vector<std::string> readFileLines(const std::string& path); // Чтение строк
};