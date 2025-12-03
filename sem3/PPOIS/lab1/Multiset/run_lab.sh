#!/bin/bash

echo "============================"
cd ~/Uni/PPOIS/lab1
g++ -std=c++17 main.cpp include/Multiset.cpp -o multiset_app

if [ $? -ne 0 ]; then
    echo " Ошибка компиляции!"
    exit 1
fi
echo "============================"
./multiset_app
