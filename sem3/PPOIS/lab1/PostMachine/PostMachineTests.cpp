#include <gtest/gtest.h>
#include "PostMachine.h"
#include <sstream>
#include <string>

// ===== Лента =====
class TapeTestSuite : public ::testing::Test {
protected:
    Tape tape;
};

TEST_F(TapeTestSuite, InitialStateIsEmpty) {
    EXPECT_EQ(tape.get(), ' ');
}

TEST_F(TapeTestSuite, SetAndReadSymbol) {
    tape.set('A');
    EXPECT_EQ(tape.get(), 'A');
}

TEST_F(TapeTestSuite, MoveRightExpandsTape) {
    tape.moveRight();
    EXPECT_EQ(tape.get(), ' ');
}

TEST_F(TapeTestSuite, MoveLeftExpandsTape) {
    tape.moveLeft();
    EXPECT_EQ(tape.get(), ' ');
}

TEST_F(TapeTestSuite, LoadFromStreamSimple) {
    std::istringstream iss("ABC");
    tape.loadFromStream(iss);
    EXPECT_EQ(tape.get(), 'A');
}

TEST_F(TapeTestSuite, LoadFromStreamWithSpaces) {
    std::istringstream iss(" 12 ");
    tape.loadFromStream(iss);
    EXPECT_EQ(tape.get(), ' ');
}

TEST_F(TapeTestSuite, ResetClearsTape) {
    tape.set('X');
    tape.reset();
    EXPECT_EQ(tape.get(), ' ');
}

TEST_F(TapeTestSuite, ComplexMovementPattern) {
    tape.set('1');
    tape.moveRight();
    tape.set('2');
    tape.moveLeft();
    EXPECT_EQ(tape.get(), '1');
}

TEST_F(TapeTestSuite, TapeExpansionRight) {
    for (int i = 0; i < 10; ++i) tape.moveRight();
    tape.set('Z');
    EXPECT_EQ(tape.get(), 'Z');
}

TEST_F(TapeTestSuite, TapeExpansionLeft) {
    for (int i = 0; i < 10; ++i) tape.moveLeft();
    tape.set('Z');
    EXPECT_EQ(tape.get(), 'Z');
}

TEST_F(TapeTestSuite, LoadEmptyStream) {
    std::istringstream iss("");
    tape.loadFromStream(iss);
    EXPECT_EQ(tape.get(), ' ');
}

TEST_F(TapeTestSuite, LoadWithSpecialCharacters) {
    std::istringstream iss("!@#$");
    tape.loadFromStream(iss);
    EXPECT_EQ(tape.get(), '!');
}

// ===== Команды =====
class CommandTestSuite : public ::testing::Test {
protected:
    PostMachineCommand cmd1{1, '0', 2, '1', 1};
    PostMachineCommand cmd2{2, '1', 1, '0', -1};
};

TEST_F(CommandTestSuite, CommandInitialization) {
    EXPECT_EQ(cmd1.getCurrentState(), 1);
    EXPECT_EQ(cmd1.getCurrentSymbol(), '0');
    EXPECT_EQ(cmd1.getNextState(), 2);
    EXPECT_EQ(cmd1.getNewSymbol(), '1');
    EXPECT_EQ(cmd1.getShift(), 1);
}

TEST_F(CommandTestSuite, MatchValidStateAndSymbol) {
    EXPECT_TRUE(cmd1.matches(1, '0'));
}

TEST_F(CommandTestSuite, MatchInvalidState) {
    EXPECT_FALSE(cmd1.matches(2, '0'));
}

TEST_F(CommandTestSuite, MatchInvalidSymbol) {
    EXPECT_FALSE(cmd1.matches(1, '1'));
}

TEST_F(CommandTestSuite, MatchDifferentCommand) {
    EXPECT_TRUE(cmd2.matches(2, '1'));
}

TEST_F(CommandTestSuite, ZeroShiftCommand) {
    PostMachineCommand cmd(1, 'X', 1, 'X', 0);
    EXPECT_EQ(cmd.getShift(), 0);
    EXPECT_TRUE(cmd.matches(1, 'X'));
}

TEST_F(CommandTestSuite, NegativeShiftCommand) {
    PostMachineCommand cmd(1, 'Y', 2, 'Y', -1);
    EXPECT_EQ(cmd.getShift(), -1);
}

TEST_F(CommandTestSuite, PositiveShiftCommand) {
    PostMachineCommand cmd(1, 'Z', 2, 'Z', 1);
    EXPECT_EQ(cmd.getShift(), 1);
}

TEST_F(CommandTestSuite, MultipleCommandInitialization) {
    PostMachineCommand cmd1(1, '0', 2, '1', 1);
    PostMachineCommand cmd2(2, '1', 1, '0', -1);
    EXPECT_NE(cmd1.getCurrentState(), cmd2.getCurrentState());
}

TEST_F(CommandTestSuite, CommandEquality) {
    PostMachineCommand cmd1(1, '0', 2, '1', 1);
    PostMachineCommand cmd2(1, '0', 2, '1', 1);
    EXPECT_EQ(cmd1.getCurrentState(), cmd2.getCurrentState());
    EXPECT_EQ(cmd1.getCurrentSymbol(), cmd2.getCurrentSymbol());
}

// ===== Тест машины =====
class MachineCoreTestSuite : public ::testing::Test {
protected:
    PostMachine machine;
};

TEST_F(MachineCoreTestSuite, InitialStateIsOne) {
    EXPECT_EQ(machine.getCurrentState(), 1);
}

TEST_F(MachineCoreTestSuite, AddRuleToEmptyMachine) {
    machine.addRule(1, 'A', 2, 'B', 1);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_NE(oss.str().find("1 A 2 B R"), std::string::npos);
}

TEST_F(MachineCoreTestSuite, LoadProgramFromStream) {
    std::istringstream iss("1 0 2 1 R\n2 1 1 0 L");
    machine.loadFromStream(iss);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_NE(oss.str().find("1 0 2 1 R"), std::string::npos);
}

TEST_F(MachineCoreTestSuite, LoadTapeFromString) {
    machine.loadTapeFromString("123");
    EXPECT_EQ(machine.getTapeSymbol(), '1');
}

TEST_F(MachineCoreTestSuite, SetTapeValue) {
    machine.setTapeValue('X');
    EXPECT_EQ(machine.getTapeSymbol(), 'X');
}

TEST_F(MachineCoreTestSuite, ResetMachine) {
    machine.setTapeValue('Y');
    machine.reset();
    EXPECT_EQ(machine.getTapeSymbol(), ' ');
    EXPECT_EQ(machine.getCurrentState(), 1);
}

TEST_F(MachineCoreTestSuite, PrintEmptyRules) {
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_EQ(oss.str(), "No rules defined\n");
}

TEST_F(MachineCoreTestSuite, PrintMultipleRules) {
    machine.addRule(1, '0', 2, '1', 1);
    machine.addRule(2, '1', 1, '0', -1);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_NE(oss.str().find("1 0 2 1 R"), std::string::npos);
}

TEST_F(MachineCoreTestSuite, LoadEmptyProgram) {
    std::istringstream iss("");
    machine.loadFromStream(iss);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_EQ(oss.str(), "No rules defined\n");
}

TEST_F(MachineCoreTestSuite, LoadProgramWithComments) {
    std::istringstream iss("# Comment\n1 0 2 1 R");
    machine.loadFromStream(iss);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_NE(oss.str().find("1 0 2 1 R"), std::string::npos);
}

TEST_F(MachineCoreTestSuite, LoadProgramWithInvalidLine) {
    std::istringstream iss("invalid line\n1 0 2 1 R");
    machine.loadFromStream(iss);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_NE(oss.str().find("1 0 2 1 R"), std::string::npos);
}

TEST_F(MachineCoreTestSuite, LoadTapeWithSpaces) {
    machine.loadTapeFromString(" 123 ");
    EXPECT_EQ(machine.getTapeSymbol(), ' ');
}

TEST_F(MachineCoreTestSuite, LoadTapeWithSpecialChars) {
    machine.loadTapeFromString("!@#$");
    EXPECT_EQ(machine.getTapeSymbol(), '!');
}

TEST_F(MachineCoreTestSuite, LoadTapeWithMixedChars) {
    machine.loadTapeFromString("A1B2");
    EXPECT_EQ(machine.getTapeSymbol(), 'A');
}

// ===== Выполнение программы =====
class MachineExecutionTestSuite : public ::testing::Test {
protected:
    PostMachine machine;
    
    void SetUp() override {
        machine.reset();
        std::istringstream iss(
            "1 0 2 1 R\n"
            "2 1 1 0 L\n"
        );
        machine.loadFromStream(iss);
    }
};

TEST_F(MachineExecutionTestSuite, StopsWhenNoRule) {
    machine.loadTapeFromString(" ");
    bool stepped = machine.step();
    EXPECT_FALSE(stepped);
}

TEST_F(MachineExecutionTestSuite, HandlesLeftMovement) {
    machine.loadTapeFromString("1");
    machine.step();
    machine.step();
    EXPECT_EQ(machine.getCurrentState(), 1);
    EXPECT_EQ(machine.getTapeSymbol(), '1');
}

TEST_F(MachineExecutionTestSuite, InfiniteLoopPrevention) {
    machine.reset();
    std::istringstream iss(
        "1 0 1 1 R\n"
        "1 1 1 0 R\n"
    );
    machine.loadFromStream(iss);
    machine.loadTapeFromString("0");
    int stepCount = 0;
    while (machine.step() && stepCount < 100) {
        stepCount++;
    }
    EXPECT_LT(stepCount, 100);
}

TEST_F(MachineExecutionTestSuite, EmptyProgramExecution) {
    machine.reset();
    machine.loadTapeFromString("123");
    machine.run(false);
    EXPECT_EQ(machine.getTapeSymbol(), '1');
}

// ===== Дополнительные тесты =====
TEST(AdditionalTests, TapeMovementConsistency) {
    Tape tape;
    tape.set('A');
    tape.moveRight();
    tape.set('B');
    tape.moveLeft();
    EXPECT_EQ(tape.get(), 'A');
}

TEST(AdditionalTests, MachineWithNoRules) {
    PostMachine machine;
    machine.loadTapeFromString("1");
    machine.run(false);
    EXPECT_EQ(machine.getTapeSymbol(), '1');
}

TEST(AdditionalTests, LargeTapeHandling) {
    PostMachine machine;
    std::string largeTape(1000, '0');
    machine.loadTapeFromString(largeTape);
    machine.moveTapeRight();
    EXPECT_EQ(machine.getTapeSymbol(), '0');
}

TEST(AdditionalTests, InvalidCharacterInProgram) {
    PostMachine machine;
    std::istringstream iss("1 X 2 Y R");
    machine.loadFromStream(iss);
    std::ostringstream oss;
    machine.printRules(oss);
    EXPECT_NE(oss.str().find("1 X 2 Y R"), std::string::npos);
}
