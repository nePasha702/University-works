#include "Deserializer.h"

Deserializer::Deserializer() 
    : format("JSON"), strictMode(true), maxDepth(5) {}

std::string Deserializer::deserialize(std::string data) {
    return "Данные из " + format + ": " + data;
}
