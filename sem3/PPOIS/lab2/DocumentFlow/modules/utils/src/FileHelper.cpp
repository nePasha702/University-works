#include "FileHelper.h"
#include <fstream>
#include <sys/stat.h>

bool FileHelper::fileExists(const std::string& path) {
    struct stat buffer;
    return (stat(path.c_str(), &buffer) == 0);
}

std::vector<std::string> FileHelper::readFileLines(const std::string& path) {
    std::vector<std::string> lines;
    std::ifstream file(path);
    if (!file.is_open()) return lines;

    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}