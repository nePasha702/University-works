#pragma once
#include <string>

class Deserializer {
private:
    std::string format;     
    bool strictMode;         
    int maxDepth;            

public:
    Deserializer();
    std::string deserialize(std::string data);
};
