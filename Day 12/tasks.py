import itertools
import math
import unittest


def main():
    with open("Day 12/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def count_brute_force(line, verbose=False):
    sequence, summary = line.split()
    count_unknowns = sum(1 for c in sequence if c == "?")
    count_possibilities = 0
    for guess in itertools.product('.#', repeat=count_unknowns):
        if get_summary(substitute_guess(sequence, guess)) == summary:
            if verbose:
                print(substitute_guess(sequence, guess))
            count_possibilities += 1
    return count_possibilities


class Cache:
    def __init__(self) -> None:
        self.possible_offsets_cache = {}
        self.recursive_count_cache = {}

    def get_possible_offsets(self, sequence, group_len, end=False):
        key = (sequence, group_len, end)
        if key in self.possible_offsets_cache:
            return self.possible_offsets_cache[key]
        else:
            self.possible_offsets_cache[key] = list(possible_offsets(
                sequence, group_len, end))
        return self.possible_offsets_cache[key]

    def get_recursive_count(self, sequence, summary):
        key = (sequence, tuple(summary))
        if key in self.recursive_count_cache:
            return self.recursive_count_cache[key]
        else:
            self.recursive_count_cache[key] = recursive_count(
                sequence, summary, self)
        return self.recursive_count_cache[key]


def count_by_sections(line, cache):
    full_sequence, full_summary = line.split()
    sections = list(filter(lambda s: s != "", full_sequence.split(".")))
    sections_possibilities = [cache.get_section_possibilities(
        section) for section in sections]
    count_combinations = math.prod(map(len, sections_possibilities))
    print(count_combinations)
    return count_combinations


def count_line_by_recursion(line, cache):
    full_sequence, full_summary = line.split()
    return recursive_count(full_sequence, list(
        map(int, full_summary.split(","))), cache)


def recursive_count(sequence, summary, cache: Cache):
    first_group_len = summary[0]
    space_for_rest = sum(summary[1:])+len(summary)-1
    

    if len(summary) == 1:
        return sum(1 for _ in cache.get_possible_offsets(sequence, first_group_len, end=True))

    try:
        if sequence[-space_for_rest] == "#":
            space_for_rest -= 1
    except IndexError:
        raise(IndexError(f"space for rest: {space_for_rest}"))

    count = 0
    for offset in cache.get_possible_offsets(sequence[:-space_for_rest], first_group_len, end=False):
        count += cache.get_recursive_count(sequence[offset +
                                 first_group_len+1:], summary[1:])
    return count


def section_possibilities(sequence):
    count_unknowns = sum(1 for c in sequence if c == "?")

    if count_unknowns == 0:
        return {get_summary(sequence): 1}

    section_summaries = {}
    for guess in itertools.product('.#', repeat=count_unknowns):
        section_summary = get_summary(substitute_guess(sequence, guess))
        section_summaries[section_summary] = section_summaries.get(
            section_summary, 0) + 1
    return section_summaries


def possible_offsets(sequence: str, group_len: int, end=False):
    for i in range(len(sequence)-group_len+1):
        if all(map(lambda char: char in ("?", "#"), sequence[i:i+group_len]))\
                and not any(map(lambda char: char == "#", sequence[:i]))\
                and safe_list_get(sequence, i+group_len, ".") in ("?", "."):
            if end == False:
                yield i
            else:
                if all(map(lambda char: char in ("?", "."), sequence[i+group_len:])):
                    yield i


def safe_list_get(l, index, default):
    try:
        return l[index]
    except IndexError:
        return default


def substitute_guess(sequence, guess: str):
    new_sequence = ""
    guess = list(guess)
    for c in sequence:
        if c == "?":
            new_sequence += guess.pop()
        else:
            new_sequence += c
    return new_sequence


def get_summary(sequence):
    count_continuous_damage = 0
    damage_groups = []
    for c in sequence:
        if c == "#":
            count_continuous_damage += 1
        if c == "." and count_continuous_damage > 0:
            damage_groups.append(count_continuous_damage)
            count_continuous_damage = 0

    if count_continuous_damage > 0:
        damage_groups.append(count_continuous_damage)

    return ",".join(map(str, damage_groups))


def unfold(line):
    sequence, summary = line.split()
    new_summary = ",".join([summary]*5)
    new_sequence = "?".join([sequence]*5)
    return " ".join((new_sequence, new_summary))


def task1(input):
    cache = Cache()
    return sum(map(lambda line: count_line_by_recursion(line, cache), input))


def task2(input):
    cache = Cache()
    return sum(map(lambda line: count_line_by_recursion(unfold(line), cache), input))


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 12/input.txt") as file:
            self.lines = list(map(str.strip, file.readlines()))
        with open("Day 12/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 12/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test_brute_force(self):
        self.assertEqual(count_brute_force("???.### 1,1,3"), 1)
        self.assertEqual(count_brute_force(".??..??...?##. 1,1,3"), 4)
        self.assertEqual(count_brute_force("?#?#?#?#?#?#?#? 1,3,1,6"), 1)
        self.assertEqual(count_brute_force("????.#...#... 4,1,1"), 1)
        self.assertEqual(count_brute_force("????.######..#####. 1,6,5"), 4)
        self.assertEqual(count_brute_force("?###???????? 3,2,1"), 10)

    def test_recursion_vs_brute_force(self):
        cache = Cache()
        self.assertEqual(count_brute_force("?????#??? 2,1,1"), 7)
        self.assertEqual(count_line_by_recursion("?????#??? 2,1,1", cache), 7)
        
        for line in self.lines:
            try:
                self.assertEqual(count_line_by_recursion(line, cache), count_brute_force(line))
            except AssertionError as e:
                print(line)
                raise e

    def test_count_line_by_recursion(self):
        cache = Cache()
        self.assertEqual(count_line_by_recursion("???.### 1,1,3", cache), 1)
        self.assertEqual(count_line_by_recursion(
            ".??..??...?##. 1,1,3", cache), 4)
        self.assertEqual(count_line_by_recursion(
            "?#?#?#?#?#?#?#? 1,3,1,6", cache), 1)
        self.assertEqual(count_line_by_recursion(
            "????.#...#... 4,1,1", cache), 1)
        self.assertEqual(count_line_by_recursion(
            "????.######..#####. 1,6,5", cache), 4)
        self.assertEqual(count_line_by_recursion(
            "?###???????? 3,2,1", cache), 10)

    def test_task1(self):
        self.assertEqual(task1(self.lines_test), 21)

    def test_unfold(self):
        self.assertEqual(unfold(".# 1"), ".#?.#?.#?.#?.# 1,1,1,1,1")
        self.assertEqual(unfold(
            "???.### 1,1,3"), "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3")

    def test_possible_offsets(self):
        self.assertEqual(list(possible_offsets(
            "??????????", 6)), [0, 1, 2, 3, 4])
        self.assertEqual(list(possible_offsets("???#?", 3)), [1, 2])
        self.assertEqual(list(possible_offsets("?#???", 3)), [0, 1])
        self.assertEqual(list(possible_offsets("??.#????", 2)), [0, 3])
        self.assertEqual(list(possible_offsets("???.###", 1)), [0,1,2])

    def test2(self):
        cache = Cache()
        self.assertEqual(count_line_by_recursion(unfold("???.### 1,1,3"), cache), 1)
        self.assertEqual(count_line_by_recursion(unfold(".??..??...?##. 1,1,3"), cache), 16384)
        self.assertEqual(count_line_by_recursion(unfold("?#?#?#?#?#?#?#? 1,3,1,6"), cache), 1)
        self.assertEqual(count_line_by_recursion(unfold("????.#...#... 4,1,1"), cache), 16)
        self.assertEqual(count_line_by_recursion(unfold("????.######..#####. 1,6,5"), cache), 2500)
        self.assertEqual(count_line_by_recursion(unfold("?###???????? 3,2,1"), cache), 506250)
        self.assertEqual(task2(self.lines_test), 525152)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
