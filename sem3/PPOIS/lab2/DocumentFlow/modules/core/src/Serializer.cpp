#include "Serializer.h"

Serializer::Serializer() 
    : format("JSON"), compress(false), version(1) {}

std::string Serializer::serialize(std::string data) {
    if (compress) data += " (сжато)";
    return "{ \"format\": \"" + format + "\", \"data\": \"" + data + "\" }";
}
