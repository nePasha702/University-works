#pragma once
#include <string>
#include <map>

class ConfigLoader {
private:
    std::string configPath;       
    std::map<std::string, std::string> settings; 
    bool isLoaded;                

public:
    ConfigLoader(std::string path);
    bool load();
    std::string getValue(std::string key);
};
