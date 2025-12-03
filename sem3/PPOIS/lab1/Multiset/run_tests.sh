#!/bin/bash

echo "=================================="
echo "🚀 ЗАПУСК ТЕСТОВ"
echo "=================================="

cd ~/Uni/PPOIS/lab1

rm -f test_app

echo "🔨 Сборка тестов"
g++ -std=c++17 - I./include -I/us/local/include tests/MultisetTests.cpp src/Multiset.cpp -o multiset_tests -L/usr/local/lib - lgtest
-lgtest_main -lpthread

if [ $? -ne 0 ]; then
    echo "❌ ОШИБКА: не удалось собрать тесты"
    exit 1
fi

echo "✅ Сборка успешна"

echo "▶️  Запуск тестов"
./test_app

echo "=================================="
echo "✅ Тесты завершены"
echo "=================================="
