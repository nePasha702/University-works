cmake_minimum_required(VERSION 3.10)
project(DocumentFlow)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Указываем корневую директорию проекта
set(PROJECT_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# Найти GoogleTest
find_package(GTest REQUIRED)
message(STATUS "Найден Google Test: ${GTEST_INCLUDE_DIRS}")

# 1. Основное приложение
add_executable(documentflow_app 
    app/main.cpp
    modules/core/src/DocumentBase.cpp
    modules/core/src/FlowController.cpp
    modules/core/src/SecurityManager.cpp
    modules/core/src/AuditLogger.cpp
    modules/core/src/StorageManager.cpp
    modules/core/src/ConfigLoader.cpp
    modules/core/src/WorkflowEngine.cpp
    modules/core/src/Validator.cpp
    modules/core/src/Serializer.cpp
    modules/core/src/Deserializer.cpp
    modules/documents/src/Contract.cpp
    modules/documents/src/Invoice.cpp
    modules/documents/src/Report.cpp
    modules/documents/src/RequestForm.cpp
    modules/documents/src/Agreement.cpp
    modules/documents/src/Order.cpp
    modules/documents/src/Memo.cpp
    modules/documents/src/Letter.cpp
    modules/documents/src/Certificate.cpp
    modules/documents/src/Policy.cpp
    modules/documents/src/Application.cpp
    modules/documents/src/Resolution.cpp
    modules/documents/src/Protocol.cpp
    modules/documents/src/Specification.cpp
    modules/documents/src/Checklist.cpp
    modules/personnel/src/Employee.cpp
    modules/personnel/src/Manager.cpp
    modules/personnel/src/Director.cpp
    modules/personnel/src/Secretary.cpp
    modules/personnel/src/Auditor.cpp
    modules/personnel/src/HRManager.cpp
    modules/personnel/src/ITSupport.cpp
    modules/personnel/src/DepartmentHead.cpp
    modules/personnel/src/Contractor.cpp
    modules/personnel/src/ExternalUser.cpp
    modules/exceptions/src/DocumentException.cpp
    modules/exceptions/src/SecurityException.cpp
    modules/exceptions/src/ValidationException.cpp
    modules/exceptions/src/WorkflowException.cpp
    modules/exceptions/src/StorageException.cpp
    modules/exceptions/src/ConfigException.cpp
    modules/exceptions/src/AuditException.cpp
    modules/exceptions/src/SerializerException.cpp
    modules/exceptions/src/DeserializerException.cpp
    modules/exceptions/src/UserException.cpp
    modules/exceptions/src/NetworkException.cpp
    modules/exceptions/src/FileException.cpp
    modules/utils/src/DateUtils.cpp
    modules/utils/src/StringUtils.cpp
    modules/utils/src/FileHelper.cpp
)

# Указываем include директории для основного приложения
target_include_directories(documentflow_app PRIVATE
    modules/core/include
    modules/documents/include
    modules/personnel/include
    modules/exceptions/include
    modules/utils/include
)

# 2. Тесты 
add_executable(documentflow_tests
    tests/DocumentFlowTests.cpp
    modules/core/src/DocumentBase.cpp
    modules/core/src/FlowController.cpp
    modules/core/src/SecurityManager.cpp
    modules/core/src/AuditLogger.cpp
    modules/core/src/StorageManager.cpp
    modules/core/src/ConfigLoader.cpp
    modules/core/src/WorkflowEngine.cpp
    modules/core/src/Validator.cpp
    modules/core/src/Serializer.cpp
    modules/core/src/Deserializer.cpp
    modules/documents/src/Contract.cpp
    modules/documents/src/Invoice.cpp
    modules/documents/src/Report.cpp
    modules/documents/src/RequestForm.cpp
    modules/documents/src/Agreement.cpp
    modules/documents/src/Order.cpp
    modules/documents/src/Memo.cpp
    modules/documents/src/Letter.cpp
    modules/documents/src/Certificate.cpp
    modules/documents/src/Policy.cpp
    modules/documents/src/Application.cpp
    modules/documents/src/Resolution.cpp
    modules/documents/src/Protocol.cpp
    modules/documents/src/Specification.cpp
    modules/documents/src/Checklist.cpp
    modules/personnel/src/Employee.cpp
    modules/personnel/src/Manager.cpp
    modules/personnel/src/Director.cpp
    modules/personnel/src/Secretary.cpp
    modules/personnel/src/Auditor.cpp
    modules/personnel/src/HRManager.cpp
    modules/personnel/src/ITSupport.cpp
    modules/personnel/src/DepartmentHead.cpp
    modules/personnel/src/Contractor.cpp
    modules/personnel/src/ExternalUser.cpp
    modules/exceptions/src/DocumentException.cpp
    modules/exceptions/src/SecurityException.cpp
    modules/exceptions/src/ValidationException.cpp
    modules/exceptions/src/WorkflowException.cpp
    modules/exceptions/src/StorageException.cpp
    modules/exceptions/src/ConfigException.cpp
    modules/exceptions/src/AuditException.cpp
    modules/exceptions/src/SerializerException.cpp
    modules/exceptions/src/DeserializerException.cpp
    modules/exceptions/src/UserException.cpp
    modules/exceptions/src/NetworkException.cpp
    modules/exceptions/src/FileException.cpp
    modules/utils/src/DateUtils.cpp
    modules/utils/src/StringUtils.cpp
    modules/utils/src/FileHelper.cpp
)

# Указываем include директории для тестов
target_include_directories(documentflow_tests PRIVATE
    modules/core/include
    modules/documents/include
    modules/personnel/include
    modules/exceptions/include
    modules/utils/include
    ${GTEST_INCLUDE_DIRS}
)

# Линкуем тесты с библиотеками
target_link_libraries(documentflow_tests
    GTest::GTest
    GTest::Main
    pthread
)

# Включаем тестирование
enable_testing()
add_test(NAME DocumentFlowTests COMMAND documentflow_tests)

message(STATUS "Тесты будут собраны: documentflow_tests")
message(STATUS "Основная программа: documentflow_app")