cmake_minimum_required(VERSION 3.10)
project(MultisetLab)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# 1. Основное приложение
add_executable(multiset_app 
    main.cpp
    src/Multiset.cpp
)

# 2. Тесты 
find_package(GTest)
if(GTest_FOUND)
    message(STATUS "Найден Google Test: ${GTEST_INCLUDE_DIRS}")
    
    add_executable(multiset_tests
        tests/MultisetTests.cpp
        src/Multiset.cpp
    )
    
    target_include_directories(multiset_tests PRIVATE ${GTEST_INCLUDE_DIRS})
    target_link_libraries(multiset_tests ${GTEST_LIBRARIES} pthread)
    
    message(STATUS "Тесты будут собраны: multiset_tests")
else()
    message(WARNING "Google Test не найден. Тесты отключены.")
endif()

message(STATUS "Основная программа: multiset_app")
