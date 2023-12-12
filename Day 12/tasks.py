import itertools
import math
import unittest
from functools import cache


def main():
    with open("Day 12/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def count_line_by_recursion(line):
    full_sequence, full_summary = line.split()
    return recursive_count(full_sequence, tuple(
        map(int, full_summary.split(","))))


@cache
def recursive_count(sequence, summary):
    first_group_len = summary[0]
    space_for_rest = sum(summary[1:])+len(summary)-1

    if len(summary) == 1:
        return sum(1 for _ in possible_offsets(sequence, first_group_len, end=True))

    if sequence[-space_for_rest] == "#":
        space_for_rest -= 1

    count = 0
    for offset in possible_offsets(sequence[:-space_for_rest], first_group_len, end=False):
        count += recursive_count(sequence[offset +
                                 first_group_len+1:], summary[1:])
    return count


@cache
def possible_offsets(sequence: str, group_len: int, end=False):
    offsets = []
    for i in range(len(sequence)-group_len+1):
        if all(map(lambda char: char in ("?", "#"), sequence[i:i+group_len]))\
                and not any(map(lambda char: char == "#", sequence[:i]))\
                and safe_list_get(sequence, i+group_len, ".") in ("?", "."):
            if end == False:
                offsets.append(i)
            else:
                if all(map(lambda char: char in ("?", "."), sequence[i+group_len:])):
                    offsets.append(i)
    return offsets


def safe_list_get(l, index, default):
    try:
        return l[index]
    except IndexError:
        return default


def unfold(line):
    sequence, summary = line.split()
    new_summary = ",".join([summary]*5)
    new_sequence = "?".join([sequence]*5)
    return " ".join((new_sequence, new_summary))


def task1(input):
    return sum(map(lambda line: count_line_by_recursion(line), input))


def task2(input):
    return sum(map(lambda line: count_line_by_recursion(unfold(line)), input))


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 12/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 12/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test_count_line_by_recursion(self):
        self.assertEqual(count_line_by_recursion("???.### 1,1,3"), 1)
        self.assertEqual(count_line_by_recursion(".??..??...?##. 1,1,3"), 4)
        self.assertEqual(count_line_by_recursion("?#?#?#?#?#?#?#? 1,3,1,6"), 1)
        self.assertEqual(count_line_by_recursion("????.#...#... 4,1,1"), 1)
        self.assertEqual(count_line_by_recursion("????.######..#####. 1,6,5"), 4)
        self.assertEqual(count_line_by_recursion("?###???????? 3,2,1"), 10)
        self.assertEqual(count_line_by_recursion("?????#??? 2,1,1"), 7)

    def test_task1(self):
        self.assertEqual(task1(self.lines_test), 21)

    def test_unfold(self):
        self.assertEqual(unfold(".# 1"), ".#?.#?.#?.#?.# 1,1,1,1,1")
        self.assertEqual(unfold("???.### 1,1,3"),
                         "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3")

    def test_possible_offsets(self):
        self.assertEqual(list(possible_offsets("??????????", 6)), [0, 1, 2, 3, 4])
        self.assertEqual(list(possible_offsets("???#?", 3)), [1, 2])
        self.assertEqual(list(possible_offsets("?#???", 3)), [0, 1])
        self.assertEqual(list(possible_offsets("??.#????", 2)), [0, 3])
        self.assertEqual(list(possible_offsets("???.###", 1)), [0, 1, 2])

    def test2(self):
        self.assertEqual(count_line_by_recursion(unfold("???.### 1,1,3")), 1)
        self.assertEqual(count_line_by_recursion(unfold(".??..??...?##. 1,1,3")), 16384)
        self.assertEqual(count_line_by_recursion(unfold("?#?#?#?#?#?#?#? 1,3,1,6")), 1)
        self.assertEqual(count_line_by_recursion(unfold("????.#...#... 4,1,1")), 16)
        self.assertEqual(count_line_by_recursion(unfold("????.######..#####. 1,6,5")), 2500)
        self.assertEqual(count_line_by_recursion(unfold("?###???????? 3,2,1")), 506250)
        self.assertEqual(task2(self.lines_test), 525152)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
