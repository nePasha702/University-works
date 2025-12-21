#pragma once
#include <string>
#include <unordered_map>
#include "DocumentBase.h"

class StorageManager {
private:
    std::string storagePath;
    std::unordered_map<std::string, DocumentBase*> documents;

public:
    StorageManager();
    void setStoragePath(const std::string& path);
    
    bool saveDocument(DocumentBase* doc);
    DocumentBase* getDocument(const std::string& id) const;
};