#ifndef MULTISET_H
#define MULTISET_H

#include <iostream>
#include <vector>
#include <memory>
#include <string>

// Объявление MultisetElement
class MultisetElement {
public:
    virtual ~MultisetElement() = default;
    virtual void print(std::ostream& os) const = 0;
    virtual std::unique_ptr<MultisetElement> clone() const = 0;
    virtual bool equals(const MultisetElement* other) const = 0;
    virtual size_t hash() const = 0;
};

// Объявление SimpleElement
class SimpleElement : public MultisetElement {
private:
    char value;
    
public:
    explicit SimpleElement(char val);
    char getValue() const;
    
    void print(std::ostream& os) const override;
    std::unique_ptr<MultisetElement> clone() const override;
    bool equals(const MultisetElement* other) const override;
    size_t hash() const override;
};

// Объявление Multiset
class Multiset : public MultisetElement {
private:
    std::vector<std::unique_ptr<MultisetElement>> elements;
    void parseFromString(const std::string& str, size_t& pos);
    void removeElementByIndex(size_t index);
    
public:
    Multiset() = default;
    Multiset(const Multiset& other);
    explicit Multiset(const std::string& str);
    explicit Multiset(const char* str);
    ~Multiset() override = default;
    
    Multiset& operator=(const Multiset& other);

    void addElement(const Multiset& element);
    void addElement(char element);
    void removeElement(char element);
    void clear();
    
    bool isEmpty() const;
    bool contains(char element) const;
    bool contains(const Multiset& element) const;
    size_t count(char element) const;
    size_t cardinality() const;
    
    bool operator==(const Multiset& other) const;
    bool operator!=(const Multiset& other) const;
    
    Multiset operator+(const Multiset& other) const;
    Multiset& operator+=(const Multiset& other);
    Multiset operator*(const Multiset& other) const;
    Multiset& operator*=(const Multiset& other);
    Multiset operator-(const Multiset& other) const;
    Multiset& operator-=(const Multiset& other);
    
    friend std::ostream& operator<<(std::ostream& os, const Multiset& multiset);
    friend std::istream& operator>>(std::istream& is, Multiset& multiset);
    
    void print(std::ostream& os) const override;
    std::unique_ptr<MultisetElement> clone() const override;
    bool equals(const MultisetElement* other) const override;
    size_t hash() const override;
    
    std::string toString() const;
};

#endif
