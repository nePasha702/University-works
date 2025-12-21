#include "ConfigLoader.h"

ConfigLoader::ConfigLoader(std::string path) 
    : configPath(path), isLoaded(false) {}

bool ConfigLoader::load() {
    // В реальном проекте здесь парсинг файла
    settings["max_documents"] = "100";
    settings["timeout"] = "30";
    isLoaded = true;
    return true;
}

std::string ConfigLoader::getValue(std::string key) {
    if (isLoaded && settings.find(key) != settings.end()) {
        return settings[key];
    }
    return "";
}