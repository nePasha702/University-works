#include "Multiset.h"
#include <gtest/gtest.h>
#include <iostream>
#include <sstream>
#include <stdexcept>

TEST(MultisetTest, DefaultConstructor) {
    Multiset m;
    EXPECT_TRUE(m.isEmpty());
    EXPECT_EQ(m.cardinality(), 0);
    EXPECT_FALSE(m.contains('a'));
    EXPECT_EQ(m.count('a'), 0);
}

TEST(MultisetTest, StringConstructorSimple) {
    Multiset m("{a, b, c}");
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('a'));
    EXPECT_TRUE(m.contains('b'));
    EXPECT_TRUE(m.contains('c'));
    EXPECT_FALSE(m.contains('d'));
}

TEST(MultisetTest, StringConstructorWithDuplicates) {
    Multiset m("{a, a, b, b, b}");
    EXPECT_EQ(m.cardinality(), 5);
    EXPECT_EQ(m.count('a'), 2);
    EXPECT_EQ(m.count('b'), 3);
    EXPECT_EQ(m.count('c'), 0);
}

TEST(MultisetTest, StringConstructorWithSpaces) {
    Multiset m("{  a ,  b  , c  }");
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('a'));
    EXPECT_TRUE(m.contains('b'));
    EXPECT_TRUE(m.contains('c'));
}

TEST(MultisetTest, StringConstructorNested) {
    Multiset m("{a, {b, c}, d}");
    EXPECT_EQ(m.cardinality(), 3);
    
    Multiset nested("{b, c}");
    EXPECT_FALSE(m.contains('b'));
    EXPECT_FALSE(m.contains('c'));
}

TEST(MultisetTest, StringConstructorDeepNested) {
    Multiset m("{{a, b}, {c, {d, e}}}");
    EXPECT_EQ(m.cardinality(), 2);
}

TEST(MultisetTest, StringConstructorInvalidFormat) {
    EXPECT_THROW(Multiset m("{a, b"), std::invalid_argument);
    EXPECT_THROW(Multiset m("a, b}"), std::invalid_argument);
    EXPECT_THROW(Multiset m("{a, b, }"), std::invalid_argument);
    EXPECT_THROW(Multiset m("{a, 1}"), std::invalid_argument);
}

TEST(MultisetTest, CharConstructor) {
    Multiset m("{x, y, z}");
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('x'));
    EXPECT_TRUE(m.contains('y'));
    EXPECT_TRUE(m.contains('z'));
}

TEST(MultisetTest, CopyConstructor) {
    Multiset m1("{x, y, z, z}");
    Multiset m2(m1);
    
    EXPECT_TRUE(m1 == m2);
    EXPECT_EQ(m1.cardinality(), m2.cardinality());
    EXPECT_EQ(m1.count('z'), m2.count('z'));
    
    m1.addElement('w');
    EXPECT_FALSE(m1 == m2);
}

TEST(MultisetTest, AssignmentOperator) {
    Multiset m1("{a, b, b}");
    Multiset m2("{c}");
    
    m2 = m1;
    EXPECT_TRUE(m1 == m2);
    EXPECT_EQ(m2.count('b'), 2);
    
    m2 = m2;
    EXPECT_TRUE(m1 == m2);
}

TEST(MultisetTest, AssignmentOperatorEmpty) {
    Multiset m1("{a, b, c}");
    Multiset m2;
    
    m2 = m1;
    EXPECT_TRUE(m1 == m2);
    
    m1 = Multiset();
    EXPECT_TRUE(m1.isEmpty());
}

TEST(MultisetTest, AddElementChar) {
    Multiset m;
    
    m.addElement('x');
    EXPECT_EQ(m.cardinality(), 1);
    EXPECT_TRUE(m.contains('x'));
    EXPECT_EQ(m.count('x'), 1);
    
    m.addElement('x');
    EXPECT_EQ(m.cardinality(), 2);
    EXPECT_EQ(m.count('x'), 2);
    
    m.addElement('y');
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('y'));
}

TEST(MultisetTest, AddElementMultiset) {
    Multiset m;
    Multiset nested("{a, b}");
    
    m.addElement(nested);
    EXPECT_EQ(m.cardinality(), 1);
    EXPECT_TRUE(m.contains(nested));
    
    m.addElement(nested);
    EXPECT_EQ(m.cardinality(), 2);
    
    EXPECT_TRUE(m.contains(nested));
    
    Multiset otherNested("{c, d}");
    EXPECT_FALSE(m.contains(otherNested));
}

TEST(MultisetTest, AddElementToNonEmpty) {
    Multiset m("{a, b}");
    
    m.addElement('c');
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('c'));
    
    Multiset nested("{x, y}");
    m.addElement(nested);
    EXPECT_EQ(m.cardinality(), 4);
    EXPECT_TRUE(m.contains(nested));
}


TEST(MultisetTest, RemoveElementExisting) {
    Multiset m("{a, a, b, c}");
    
    m.removeElement('a');
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_EQ(m.count('a'), 1);
    
    m.removeElement('a');
    EXPECT_EQ(m.cardinality(), 2);
    EXPECT_EQ(m.count('a'), 0);
    EXPECT_FALSE(m.contains('a'));
    
    m.removeElement('b');
    EXPECT_EQ(m.cardinality(), 1);
    EXPECT_FALSE(m.contains('b'));
}

TEST(MultisetTest, RemoveElementNonExisting) {
    Multiset m("{a, b, c}");
    
    EXPECT_NO_THROW(m.removeElement('x'));
    EXPECT_EQ(m.cardinality(), 3);
    
    Multiset empty;
    EXPECT_NO_THROW(empty.removeElement('a'));
    EXPECT_TRUE(empty.isEmpty());
}

TEST(MultisetTest, RemoveElementFromEmpty) {
    Multiset m;
    m.removeElement('a');
    EXPECT_TRUE(m.isEmpty());
}

TEST(MultisetTest, Clear) {
    Multiset m("{a, b, c, c, d}");
    
    EXPECT_FALSE(m.isEmpty());
    m.clear();
    EXPECT_TRUE(m.isEmpty());
    EXPECT_EQ(m.cardinality(), 0);
    EXPECT_FALSE(m.contains('a'));
    EXPECT_EQ(m.count('c'), 0);
    
    Multiset empty;
    empty.clear();
    EXPECT_TRUE(empty.isEmpty());
}

TEST(MultisetTest, ContainsChar) {
    Multiset m("{a, b, b, c}");
    
    EXPECT_TRUE(m.contains('a'));
    EXPECT_TRUE(m.contains('b'));
    EXPECT_TRUE(m.contains('c'));
    EXPECT_FALSE(m.contains('d'));
    EXPECT_FALSE(m.contains('x'));
    
    Multiset empty;
    EXPECT_FALSE(empty.contains('a'));
}

TEST(MultisetTest, ContainsMultiset) {
    Multiset m("{a, {b, c}, d}");
    Multiset nested("{b, c}");
    Multiset otherNested("{x, y}");
    Multiset deepNested("{{e, f}}");
    
    EXPECT_TRUE(m.contains(nested));
    EXPECT_FALSE(m.contains(otherNested));
    
    m.addElement(deepNested);
    EXPECT_TRUE(m.contains(deepNested));
}

TEST(MultisetTest, CountElements) {
    Multiset m("{a, a, a, b, b, c}");
    
    EXPECT_EQ(m.count('a'), 3);
    EXPECT_EQ(m.count('b'), 2);
    EXPECT_EQ(m.count('c'), 1);
    EXPECT_EQ(m.count('d'), 0);
    EXPECT_EQ(m.count('x'), 0);
    
    Multiset empty;
    EXPECT_EQ(empty.count('a'), 0);
}

TEST(MultisetTest, CardinalityVarious) {
    Multiset empty("{}");
    EXPECT_EQ(empty.cardinality(), 0);
    
    Multiset single("{a}");
    EXPECT_EQ(single.cardinality(), 1);
    
    Multiset withDuplicates("{a, a, a}");
    EXPECT_EQ(withDuplicates.cardinality(), 3);
    
    Multiset nested("{a, {b, c}}");
    EXPECT_EQ(nested.cardinality(), 2);
    
    Multiset complex("{a, a, {b, c}, {b, c}, d}");
    EXPECT_EQ(complex.cardinality(), 5);
}

TEST(MultisetTest, IsEmpty) {
    Multiset empty;
    EXPECT_TRUE(empty.isEmpty());
    
    Multiset nonEmpty("{a}");
    EXPECT_FALSE(nonEmpty.isEmpty());
    
    nonEmpty.clear();
    EXPECT_TRUE(nonEmpty.isEmpty());
}


TEST(MultisetTest, EqualityOperator) {
    Multiset m1("{a, b, c}");
    Multiset m2("{c, b, a}");
    Multiset m3("{a, b}");
    Multiset m4("{a, a, b}");
    Multiset m5("{a, b, c, c}");
    
    EXPECT_TRUE(m1 == m2);
    EXPECT_FALSE(m1 == m3);
    EXPECT_FALSE(m1 == m4);
    EXPECT_FALSE(m1 == m5);
    
    Multiset n1("{a, {b, c}}");
    Multiset n2("{{b, c}, a}");
    EXPECT_TRUE(n1 == n2);
}

TEST(MultisetTest, InequalityOperator) {
    Multiset m1("{a, b, c}");
    Multiset m2("{a, b}");
    Multiset m3("{a, b, d}");
    
    EXPECT_TRUE(m1 != m2);
    EXPECT_TRUE(m1 != m3);
    
    Multiset same("{c, b, a}");
    EXPECT_FALSE(m1 != same);
}

TEST(MultisetTest, UnionSimple) {
    Multiset m1("{a, b}");
    Multiset m2("{b, c}");
    Multiset result = m1 + m2;
    
    EXPECT_EQ(result.cardinality(), 4);
    EXPECT_EQ(result.count('a'), 1);
    EXPECT_EQ(result.count('b'), 2);
    EXPECT_EQ(result.count('c'), 1);
    
    Multiset m3 = m1;
    m3 += m2;
    EXPECT_TRUE(m3 == result);
}

TEST(MultisetTest, UnionWithEmpty) {
    Multiset m1("{a, b, c}");
    Multiset empty;
    
    Multiset result1 = m1 + empty;
    EXPECT_TRUE(result1 == m1);
    
    Multiset result2 = empty + m1;
    EXPECT_TRUE(result2 == m1);
    
    Multiset result3 = empty + empty;
    EXPECT_TRUE(result3.isEmpty());
}

TEST(MultisetTest, UnionWithDuplicates) {
    Multiset m1("{a, a, b}");
    Multiset m2("{a, b, b, c}");
    Multiset result = m1 + m2;
    
    EXPECT_EQ(result.cardinality(), 7);
    EXPECT_EQ(result.count('a'), 3);
    EXPECT_EQ(result.count('b'), 3);
    EXPECT_EQ(result.count('c'), 1);
}

TEST(MultisetTest, UnionWithNested) {
    Multiset m1("{a, {b, c}}");
    Multiset m2("{d, {b, c}}");
    Multiset result = m1 + m2;
    
    EXPECT_EQ(result.cardinality(), 4);
    EXPECT_TRUE(result.contains(Multiset("{b, c}")));
    EXPECT_EQ(result.count('a'), 1);
    EXPECT_EQ(result.count('d'), 1);
}

TEST(MultisetTest, IntersectionSimple) {
    Multiset m1("{a, b, c, c}");
    Multiset m2("{b, c, d, d}");
    Multiset result = m1 * m2;
    
    EXPECT_EQ(result.cardinality(), 2);  // b, c
    EXPECT_EQ(result.count('a'), 0);
    EXPECT_EQ(result.count('b'), 1);
    EXPECT_EQ(result.count('c'), 1);
    EXPECT_EQ(result.count('d'), 0);
    
    Multiset m3 = m1;
    m3 *= m2;
    EXPECT_TRUE(m3 == result);
}

TEST(MultisetTest, IntersectionWithEmpty) {
    Multiset m1("{a, b, c}");
    Multiset empty;
    
    Multiset result1 = m1 * empty;
    EXPECT_TRUE(result1.isEmpty());
    
    Multiset result2 = empty * m1;
    EXPECT_TRUE(result2.isEmpty());
    
    Multiset result3 = empty * empty;
    EXPECT_TRUE(result3.isEmpty());
}

TEST(MultisetTest, IntersectionNoCommon) {
    Multiset m1("{a, a, b}");
    Multiset m2("{c, c, d}");
    Multiset result = m1 * m2;
    
    EXPECT_TRUE(result.isEmpty());
    EXPECT_EQ(result.cardinality(), 0);
}

TEST(MultisetTest, IntersectionWithNested) {
    Multiset m1("{a, {b, c}, d}");
    Multiset m2("{{b, c}, d, e}");
    Multiset result = m1 * m2;
    
    EXPECT_EQ(result.cardinality(), 2);
    EXPECT_TRUE(result.contains(Multiset("{b, c}")));
    EXPECT_TRUE(result.contains('d'));
    EXPECT_FALSE(result.contains('a'));
    EXPECT_FALSE(result.contains('e'));
}

TEST(MultisetTest, DifferenceSimple) {
    Multiset m1("{a, b, c, c, d}");
    Multiset m2("{b, c, e}");
    Multiset result = m1 - m2;
    
    EXPECT_EQ(result.cardinality(), 3);
    EXPECT_EQ(result.count('a'), 1);
    EXPECT_EQ(result.count('b'), 0);
    EXPECT_EQ(result.count('c'), 1);
    EXPECT_EQ(result.count('d'), 1);
    EXPECT_EQ(result.count('e'), 0);
    
    Multiset m3 = m1;
    m3 -= m2;
    EXPECT_TRUE(m3 == result);
}

TEST(MultisetTest, DifferenceWithEmpty) {
    Multiset m1("{a, b, c}");
    Multiset empty;
    
    Multiset result1 = m1 - empty;
    EXPECT_TRUE(result1 == m1);
    
    Multiset result2 = empty - m1;
    EXPECT_TRUE(result2.isEmpty());
    
    Multiset result3 = empty - empty;
    EXPECT_TRUE(result3.isEmpty());
}

TEST(MultisetTest, DifferenceRemoveAll) {
    Multiset m1("{a, a, a, b}");
    Multiset m2("{a, a}");
    Multiset result = m1 - m2;
    
    EXPECT_EQ(result.cardinality(), 2);
    EXPECT_EQ(result.count('a'), 1);
    EXPECT_EQ(result.count('b'), 1);
}

TEST(MultisetTest, DifferenceEverything) {
    Multiset m1("{a, b, c}");
    Multiset m2("{a, b, c}");
    Multiset result = m1 - m2;
    
    EXPECT_TRUE(result.isEmpty());
    EXPECT_EQ(result.cardinality(), 0);
}

TEST(MultisetTest, OutputOperator) {
    Multiset m("{a, b, c}");
    std::ostringstream oss;
    oss << m;
    
    std::string output = oss.str();
    EXPECT_FALSE(output.empty());
    EXPECT_EQ(output[0], '{');
    EXPECT_EQ(output[output.length()-1], '}');
    
    Multiset empty;
    std::ostringstream oss2;
    oss2 << empty;
    EXPECT_EQ(oss2.str(), "{}");
}

TEST(MultisetTest, OutputOperatorWithNested) {
    Multiset m("{a, {b, c}}");
    std::ostringstream oss;
    oss << m;
    
    std::string output = oss.str();
    EXPECT_NE(output.find("{b, c}"), std::string::npos);
}

TEST(MultisetTest, InputOperator) {
    std::istringstream iss("{x, y, z}");
    Multiset m;
    iss >> m;
    
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('x'));
    EXPECT_TRUE(m.contains('y'));
    EXPECT_TRUE(m.contains('z'));
}

TEST(MultisetTest, InputOperatorWithSpaces) {
    std::istringstream iss("  {  a  ,  b  ,  c  }  ");
    Multiset m;
    iss >> m;
    
    EXPECT_EQ(m.cardinality(), 3);
    EXPECT_TRUE(m.contains('a'));
    EXPECT_TRUE(m.contains('b'));
    EXPECT_TRUE(m.contains('c'));
}


TEST(MultisetTest, ToString) {
    Multiset m("{a, b, c}");
    std::string str = m.toString();
    
    EXPECT_FALSE(str.empty());
    EXPECT_EQ(str[0], '{');
    EXPECT_EQ(str[str.length()-1], '}');
    EXPECT_NE(str.find('a'), std::string::npos);
    EXPECT_NE(str.find('b'), std::string::npos);
    EXPECT_NE(str.find('c'), std::string::npos);
}

TEST(MultisetTest, HashFunction) {
    Multiset m1("{a, b, c}");
    Multiset m2("{a, b, c}");
    Multiset m3("{a, b}");
    
    EXPECT_EQ(m1.hash(), m2.hash());
    EXPECT_NE(m1.hash(), m3.hash());
}

TEST(MultisetTest, EqualsMethod) {
    Multiset m1("{a, b, c}");
    Multiset m2("{c, b, a}");
    Multiset m3("{a, b}");
    
    std::unique_ptr<MultisetElement> elem1 = m1.clone();
    std::unique_ptr<MultisetElement> elem2 = m2.clone();
    std::unique_ptr<MultisetElement> elem3 = m3.clone();
    
    EXPECT_TRUE(elem1->equals(elem2.get()));
    EXPECT_FALSE(elem1->equals(elem3.get()));
}

TEST(MultisetTest, CloneMethod) {
    Multiset original("{a, {b, c}, d}");
    std::unique_ptr<MultisetElement> clone = original.clone();
    
    Multiset* clonedMultiset = dynamic_cast<Multiset*>(clone.get());
    ASSERT_NE(clonedMultiset, nullptr);
    
    EXPECT_TRUE(original == *clonedMultiset);
    EXPECT_EQ(original.cardinality(), clonedMultiset->cardinality());
}

TEST(MultisetTest, LargeMultiset) {
    std::string input = "{";
    for (int i = 0; i < 10; ++i) {
        if (i > 0) input += ", ";
        input += std::string(1, 'a' + i);
    }
    input += "}";
    
    Multiset m(input);
    EXPECT_EQ(m.cardinality(), 10);
    for (char c = 'a'; c < 'a' + 10; ++c) {
        EXPECT_TRUE(m.contains(c));
    }
}

TEST(MultisetTest, ComplexNesting) {
    Multiset m("{{{{a}}}, b, {c, {d, e}}}");
    EXPECT_GT(m.cardinality(), 0);
}

TEST(SimpleElementTest, ConstructorAndGetValue) {
    SimpleElement se('x');
    EXPECT_EQ(se.getValue(), 'x');
}

TEST(SimpleElementTest, Equals) {
    SimpleElement se1('a');
    SimpleElement se2('a');
    SimpleElement se3('b');
    
    EXPECT_TRUE(se1.equals(&se2));
    EXPECT_FALSE(se1.equals(&se3));
    
    Multiset m("{a, b}");
    EXPECT_FALSE(se1.equals(&m));
}

TEST(SimpleElementTest, Print) {
    SimpleElement se('z');
    std::ostringstream oss;
    se.print(oss);
    EXPECT_EQ(oss.str(), "z");
}

TEST(SimpleElementTest, Clone) {
    SimpleElement original('x');
    std::unique_ptr<MultisetElement> clone = original.clone();
    
    SimpleElement* clonedSe = dynamic_cast<SimpleElement*>(clone.get());
    ASSERT_NE(clonedSe, nullptr);
    EXPECT_EQ(clonedSe->getValue(), 'x');
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
