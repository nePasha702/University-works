#include "SecurityManager.h"

SecurityManager::SecurityManager() 
    : isLocked(false) {}

void SecurityManager::setUser(std::string user) {
    currentUser = user;
}

bool SecurityManager::checkAccess(std::string requiredRole) {
    for (const auto& role : roles) {
        if (role == requiredRole) return true;
    }
    return false;
}

void SecurityManager::lockSystem() {
    isLocked = true;
}
