import unittest
from dataclasses import dataclass
import regex


def main():
    with open("Day 5/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


@dataclass
class MapPiece:
    y: int
    x: int
    length: int


class Map:
    def __init__(self, lines) -> None:
        self.pieces = []
        for line in lines:
            self.pieces.append(MapPiece(*list(map(int, line.split(" ")))))
        self.jump_points = []
        for piece in self.pieces:
            self.jump_points.append(piece.x - 1)
            self.jump_points.append(piece.x)
            self.jump_points.append(piece.x + piece.length)
            self.jump_points.append(piece.x + piece.length + 1)

    def forwards(self, x):
        for piece in self.pieces:
            if piece.x <= x < piece.x + piece.length:
                return piece.y - piece.x + x
        return x

    def backwards(self, y):
        for piece in self.pieces:
            if piece.y <= y < piece.y + piece.length:
                return piece.x - piece.y + y
        return y


def extract_seeds_maps(input_lines):
    maps = []
    text_input = "\n".join(input_lines)
    maps_text = regex.findall(r'\d[0-9 \n]+(?=\n)', text_input)
    for map_text in maps_text[1:]:
        maps.append(Map(map_text.splitlines()))
    seeds = list(map(int, maps_text[0].split(" ")))
    return seeds, maps


def forward_track(soil, maps):
    mapped = soil
    for m in maps:
        mapped = m.forwards(mapped)
    return mapped


def task1(lines):
    seeds, maps = extract_seeds_maps(input_lines=lines)
    locations = list(map(lambda s: forward_track(s, maps), seeds))
    return min(locations)


def is_in_seed_range(n, seeds):
    for i in range(0, len(seeds), 2):
        if seeds[i] <= n < seeds[i] + seeds[i+1]:
            return True
    return False


def task2(lines):
    def backtrack_jump_points():
        jump_points = []
        for m in reversed(maps):
            new_jump_points = list(map(m.backwards, jump_points))
            new_jump_points += m.jump_points
            jump_points = list(set(new_jump_points))
        return jump_points

    seeds, maps = extract_seeds_maps(input_lines=lines)

    interesting_seeds = list(
        filter(lambda p: is_in_seed_range(p, seeds), backtrack_jump_points()))
    for i in range(0, len(seeds), 2):
        interesting_seeds.append(seeds[i])
        interesting_seeds.append(seeds[i] + seeds[i+1])

    locations = list(map(lambda s: forward_track(s, maps), interesting_seeds))
    return min(locations)


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 5/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 35)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 46)

    def test_map_forwards(self):
        m = Map(["5 0 2", "15 40 1"])
        self.assertEqual(m.forwards(0), 5)
        self.assertEqual(m.forwards(1), 6)
        self.assertEqual(m.forwards(2), 2)

        self.assertEqual(m.forwards(40), 15)
        self.assertEqual(m.forwards(41), 41)

    def test_map_backwards(self):
        m = Map(["5 0 2", "15 40 1"])
        self.assertEqual(m.backwards(5), 0)
        self.assertEqual(m.backwards(6), 1)
        self.assertEqual(m.backwards(2), 2)

        self.assertEqual(m.backwards(15), 40)
        self.assertEqual(m.backwards(41), 41)

    def test_is_in_seed_range(self):
        self.assertEqual(is_in_seed_range(78, [79, 14, 55, 13]), False)
        self.assertEqual(is_in_seed_range(79, [79, 14, 55, 13]), True)
        self.assertEqual(is_in_seed_range(92, [79, 14, 55, 13]), True)
        self.assertEqual(is_in_seed_range(93, [79, 14, 55, 13]), False)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
