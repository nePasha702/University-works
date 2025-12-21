#include "StorageManager.h"

StorageManager::StorageManager() : storagePath("default_storage") {}

void StorageManager::setStoragePath(const std::string& path) {
    storagePath = path;
}

bool StorageManager::saveDocument(DocumentBase* doc) {
    if (documents.find(doc->getId()) != documents.end()) {
        return false;
    }
    documents[doc->getId()] = doc;
    return true;
}

DocumentBase* StorageManager::getDocument(const std::string& id) const {
    auto it = documents.find(id);
    return (it != documents.end()) ? it->second : nullptr;
}