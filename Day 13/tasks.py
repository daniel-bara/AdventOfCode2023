import math
import unittest


def main():
    with open("Day 13/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")

def search_vertical_mirror(lines) -> int:
    offsets = test_vertical_mirror_offsets(lines[0])
    for line in lines[1:]:
        if not offsets:
            return 0
        offsets = test_vertical_mirror_offsets(line, offsets)
    return safe_get(offsets, 0, 0)

def test_vertical_mirror_offsets(line, offsets=None):
    if offsets is None:
        offsets = range(1, len(line))
    return list(filter(lambda offset: is_iterable_mirrored(line, offset), offsets))

def is_iterable_mirrored(line, offset):
    for i in range(math.ceil(abs(len(line)/2))):
        char_to_right = safe_get(line, offset+i, None)
        char_to_left = safe_get(line, offset-i-1, None)
        if char_to_right is not None and char_to_left is not None and char_to_left != char_to_right:
            return False
    return True

def search_horizontal_mirror(lines) -> int:
    for offset in range(1, len(lines)):
        if is_iterable_mirrored(lines, offset):
            return offset
    return 0


def is_iterable_smudge_mirrored(line, offset):
    count_mismatches = 0
    for i in range(math.ceil(abs(len(line)/2))):
        item_to_right = safe_get(line, offset+i, None)
        item_to_left = safe_get(line, offset-i-1, None)
        if item_to_right is not None and item_to_left is not None :
            if item_to_left != item_to_right:
                if len(item_to_left) == 1:
                    count_mismatches += 1
                else:
                    count_mismatches += sum(1 for i in range(len(item_to_left)) if item_to_left[i] != item_to_right[i])
    return count_mismatches == 1

def search_horizontal_smudged_mirror(lines) -> int:
    for offset in range(1, len(lines)):
        if is_iterable_smudge_mirrored(lines, offset):
            return offset
    return 0

def test_offset_vertical_smudge_mirrored(lines, offset):
    count_mismatches = 0
    for line in lines:
        smudge_mirrored = is_iterable_smudge_mirrored(line, offset)
        if not smudge_mirrored and not is_iterable_mirrored(line, offset):
            return False
        if smudge_mirrored:
            count_mismatches += 1
    return count_mismatches == 1


def search_vertical_smudged_mirror(lines) -> int:
    possible_offsets = list(range(1, len(lines[0])))
    smudged_offsets = list(filter(lambda o: test_offset_vertical_smudge_mirrored(lines, o), possible_offsets))
    return safe_get(smudged_offsets, 0, 0)



def safe_get (iterable, index, default):
  if index < 0:
      return default
  try:
    return iterable[index]
  except IndexError:
    return default

def task1(task_lines):
    fields_str = "\n".join(task_lines).split("\n\n")
    fields = list(map(lambda field: field.split("\n"), fields_str))
    return sum(map(lambda field: search_horizontal_mirror(field)*100 + search_vertical_mirror(field), fields))


def task2(task_lines):
    fields_str = "\n".join(task_lines).split("\n\n")
    fields = list(map(lambda field: field.split("\n"), fields_str))
    return sum(map(lambda field: search_horizontal_smudged_mirror(field)*100 + search_vertical_smudged_mirror(field), fields))


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 13/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test_is_iterable_mirrored(self):
        self.assertEqual(is_iterable_mirrored("abba", 2), True)
        self.assertEqual(is_iterable_mirrored("abba", 1), False)
        self.assertEqual(is_iterable_mirrored("aba", 1), False)
        self.assertEqual(is_iterable_mirrored("baa", 2), True)
        self.assertEqual(is_iterable_mirrored("aba", 2), False)

        self.assertEqual(is_iterable_mirrored(".-####-", 4), True)


    def test_search_vertical_mirror(self):
        self.assertEqual(search_vertical_mirror(["####", "aabc"]), 1)
        self.assertEqual(search_vertical_mirror(["####", "abcd"]), 0)

    def test_search_horizontal_mirror(self):
        self.assertEqual(search_horizontal_mirror(["ab", "aa", "aa", "ab"]), 2)

    def test_is_iterable_smudge_mirrored(self):
        self.assertEqual(is_iterable_smudge_mirrored("abbk", 2), True)
        self.assertEqual(is_iterable_smudge_mirrored("abba", 1), True)
        self.assertEqual(is_iterable_smudge_mirrored("abaaaaa", 2), True)
        self.assertEqual(is_iterable_smudge_mirrored("aaaa", 2), False)
        self.assertEqual(is_iterable_smudge_mirrored("aba", 2), True)
        self.assertEqual(is_iterable_smudge_mirrored(".-###/-.", 4), True)

    def test_search_vertical_smudged_mirror(self):
        self.assertEqual(search_vertical_smudged_mirror(["####aa", "....rt"]), 5)
        self.assertEqual(search_vertical_smudged_mirror(["...##....", ".#.##....", "abbbbbbaa"]), 4)


    def test(self):
        self.assertEqual(task1(self.lines_test), 405)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 400)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
