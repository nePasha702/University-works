cmake_minimum_required(VERSION 3.10)
project(PostMachine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# 1. Основное приложение
add_executable(postmachine_app 
    main.cpp
    src/Menu.cpp
    src/PostMachine.cpp
    src/PostMachineCommand.cpp
    src/PostMachineTape.cpp
)

# 2. Тесты 
find_package(GTest REQUIRED)
message(STATUS "Найден Google Test: ${GTEST_INCLUDE_DIRS}")

add_executable(postmachine_tests
    tests/PostMachineTests.cpp
    src/PostMachine.cpp
    src/PostMachineCommand.cpp
    src/PostMachineTape.cpp
)

target_include_directories(postmachine_tests PRIVATE ${GTEST_INCLUDE_DIRS})
target_link_libraries(postmachine_tests 
    ${GTEST_LIBRARIES} 
    ${GTEST_MAIN_LIBRARIES}
    pthread
)

message(STATUS "Тесты будут собраны: postmachine_tests")
message(STATUS "Основная программа: postmachine_app")
