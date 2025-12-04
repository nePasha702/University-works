#include "Multiset.h"

#include <sstream>
#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <functional>


SimpleElement::SimpleElement(char val) : value(val) {}

char SimpleElement::getValue() const {
    return value;
}

void SimpleElement::print(std::ostream& os) const {
    os << value;
}

std::unique_ptr<MultisetElement> SimpleElement::clone() const {
    return std::make_unique<SimpleElement>(value);
}

bool SimpleElement::equals(const MultisetElement* other) const {
    if (auto se = dynamic_cast<const SimpleElement*>(other)) {
        return value == se->value;
    }
    return false;
}

size_t SimpleElement::hash() const {
    return std::hash<char>()(value);
}


static void skipSpaces(const std::string& str, size_t& pos) {
    while (pos < str.length() && std::isspace(str[pos])) {
        ++pos;
    }
}

void Multiset::parseFromString(const std::string& str, size_t& pos) {
    skipSpaces(str, pos);
    
    if (pos >= str.length() || str[pos] != '{') {
        throw std::invalid_argument("Invalid multiset format: expected '{'");
    }
    
    ++pos;
    
    while (pos < str.length() && str[pos] != '}') {
        skipSpaces(str, pos);
        
        if (str[pos] == '{') {
            Multiset nested;
            nested.parseFromString(str, pos);
            elements.push_back(std::make_unique<Multiset>(std::move(nested)));
        } else if (std::isalpha(str[pos])) {
            elements.push_back(std::make_unique<SimpleElement>(str[pos]));
            ++pos;
        } else if (str[pos] == '(' && pos + 1 < str.length() && str[pos + 1] == ')') {
            elements.push_back(std::make_unique<Multiset>());
            pos += 2;
        } else {
            throw std::invalid_argument("Invalid character in multiset");
        }
        
        skipSpaces(str, pos);
        
        if (pos < str.length() && str[pos] != '}' && str[pos] != ',') {
            throw std::invalid_argument("Expected ',' or '}'");
        }
        
        if (pos < str.length() && str[pos] == ',') {
            ++pos;
        }
    }
    
    if (pos >= str.length() || str[pos] != '}') {
        throw std::invalid_argument("Invalid multiset format: expected '}'");
    }
    
    ++pos;
}

Multiset::Multiset(const Multiset& other) {
    for (const auto& elem : other.elements) {
        elements.push_back(elem->clone());
    }
}

Multiset::Multiset(const std::string& str) {
    size_t pos = 0;
    parseFromString(str, pos);
    
    skipSpaces(str, pos);
    if (pos != str.length()) {
        throw std::invalid_argument("Extra characters after multiset");
    }
}

Multiset::Multiset(const char* str) : Multiset(std::string(str)) {}

Multiset& Multiset::operator=(const Multiset& other) {
    if (this != &other) {
        clear();
        for (const auto& elem : other.elements) {
            elements.push_back(elem->clone());
        }
    }
    return *this;
}   

void Multiset::addElement(char element) {
    elements.push_back(std::make_unique<SimpleElement>(element));
}

void Multiset::addElement(const Multiset& element) {
    elements.push_back(std::make_unique<Multiset>(element));
}

void Multiset::removeElement(char element) {
    for (size_t i = 0; i < elements.size(); ++i) {
        if (auto se = dynamic_cast<SimpleElement*>(elements[i].get())) {
            if (se->getValue() == element) {
                removeElementByIndex(i);
                return;
            }
        }
    }
}

void Multiset::removeElementByIndex(size_t index) {
    if (index < elements.size()) {
        elements.erase(elements.begin() + index);
    }
}

void Multiset::clear() {
    elements.clear();
}

bool Multiset::isEmpty() const {
    return elements.empty();
}

bool Multiset::contains(char element) const {
    for (const auto& elem : elements) {
        if (auto se = dynamic_cast<const SimpleElement*>(elem.get())) {
            if (se->getValue() == element) {
                return true;
            }
        }
    }
    return false;
}

bool Multiset::contains(const Multiset& element) const {
    for (const auto& elem : elements) {
        if (auto ms = dynamic_cast<const Multiset*>(elem.get())) {
            if (*ms == element) {
                return true;
            }
        }
    }
    return false;
}

size_t Multiset::cardinality() const {
    return elements.size();
}

size_t Multiset::count(char element) const {
    size_t cnt = 0;
    for (const auto& elem : elements) {
        if (auto se = dynamic_cast<const SimpleElement*>(elem.get())) {
            if (se->getValue() == element) {
                ++cnt;
            }
        }
    }
    return cnt;
}

bool Multiset::operator==(const Multiset& other) const {
    if (elements.size() != other.elements.size()) {
        return false;
    }
    
    std::vector<bool> used(other.elements.size(), false);
    
    for (const auto& elem : elements) {
        bool found = false;
        for (size_t j = 0; j < other.elements.size(); ++j) {
            if (!used[j] && elem->equals(other.elements[j].get())) {
                used[j] = true;
                found = true;
                break;
            }
        }
        if (!found) {
            return false;
        }
    }
    
    return true;
}

bool Multiset::operator!=(const Multiset& other) const {
    return !(*this == other);
}

Multiset Multiset::operator+(const Multiset& other) const {
    Multiset result = *this;
    result += other;
    return result;
}

Multiset& Multiset::operator+=(const Multiset& other) {
    for (const auto& elem : other.elements) {
        elements.push_back(elem->clone());
    }
    return *this;
}

Multiset Multiset::operator*(const Multiset& other) const {
    
    Multiset result;
    
    std::vector<std::unique_ptr<MultisetElement>> otherElements;
    for (const auto& elem : other.elements) {
        otherElements.push_back(elem->clone());
    }
    
    for (const auto& elem : elements) {
        for (auto& otherElem : otherElements) {
            if (otherElem && elem->equals(otherElem.get())) {
                result.elements.push_back(elem->clone());
                otherElem.reset();
                break;
            }
        }
    }
    
    return result;
}

Multiset& Multiset::operator*=(const Multiset& other) {
    *this = *this * other;
    return *this;
}

Multiset Multiset::operator-(const Multiset& other) const {
    Multiset result;
    
    std::vector<std::unique_ptr<MultisetElement>> otherElements;
    for (const auto& elem : other.elements) {
        otherElements.push_back(elem->clone());
    }
    
    for (const auto& elem : elements) {
        bool found = false;
        for (auto& otherElem : otherElements) {
            if (otherElem && elem->equals(otherElem.get())) {
                otherElem.reset();
                found = true;
                break;
            }
        }
        if (!found) {
            result.elements.push_back(elem->clone());
        }
    }
    
    return result;
}

Multiset& Multiset::operator-=(const Multiset& other) {
    *this = *this - other;
    return *this;
}

void Multiset::print(std::ostream& os) const {
    os << "{";
    for (size_t i = 0; i < elements.size(); ++i) {
        if (i > 0) {
            os << ", ";
        }
        elements[i]->print(os);
    }
    os << "}";
}

std::ostream& operator<<(std::ostream& os, const Multiset& multiset) {
    multiset.print(os);
    return os;
}

std::istream& operator>>(std::istream& is, Multiset& multiset) {
    std::string str;
    std::getline(is, str);
    multiset = Multiset(str);
    return is;
}

std::unique_ptr<MultisetElement> Multiset::clone() const {
    return std::make_unique<Multiset>(*this);
}

bool Multiset::equals(const MultisetElement* other) const {
    if (auto ms = dynamic_cast<const Multiset*>(other)) {
        return *this == *ms;
    }
    return false;
}

size_t Multiset::hash() const {
    size_t h = 0;
    for (const auto& elem : elements) {
        h ^= elem->hash() + 0x9e3779b9 + (h << 6) + (h >> 2);
    }
    return h;
}

std::string Multiset::toString() const {
    std::ostringstream oss;
    oss << *this;
    return oss.str();
}
