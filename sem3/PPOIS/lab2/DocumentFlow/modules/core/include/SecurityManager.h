    #pragma once
    #include <string>
    #include <vector>

    // Контроль доступа
    class SecurityManager {
    private:
        std::string currentUser;       // Текущий пользователь
        std::vector<std::string> roles; // Роли пользователя
        bool isLocked;                 // Блокировка системы

    public:
        SecurityManager();
        void setUser(std::string user);
        bool checkAccess(std::string requiredRole);
        void lockSystem();
    };