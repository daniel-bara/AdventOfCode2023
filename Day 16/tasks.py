from dataclasses import dataclass
import time
import unittest


def main():
    with open("Day 16/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


LEFT = (-1, 0)
UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)


@dataclass
class LightBeam:
    direction: tuple


class Tile:
    def __init__(self, c: str) -> None:
        self.character = c
        self.reset_energy()

    def reset_energy(self):
        self.energy = {UP: False, DOWN: False, LEFT: False, RIGHT: False}

    def is_energised(self):
        return any(self.energy.values())

    def is_energised_in_direction(self, direction):
        return self.energy[direction]

    def energise_in_direction(self, direction):
        self.energy[direction] = True

    def __str__(self) -> str:
        if self.is_energised():
            return "#"
        return self.character

    def route(self):
        raise Exception("This is an abstract method")


class Air(Tile):
    def route(self, light: LightBeam) -> list[LightBeam]:
        return [light]


class Mirror(Tile):
    def route(self, light: LightBeam) -> list[LightBeam]:
        match (self.character):
            case "-":
                if light.direction in (LEFT, RIGHT):
                    return [light]
                else:
                    return [LightBeam(LEFT), LightBeam(RIGHT)]
            case "|":
                if light.direction in (UP, DOWN):
                    return [light]
                else:
                    return [LightBeam(UP), LightBeam(DOWN)]
            case "/":
                if light.direction == UP:
                    return [LightBeam(RIGHT)]
                if light.direction == LEFT:
                    return [LightBeam(DOWN)]
                if light.direction == DOWN:
                    return [LightBeam(LEFT)]
                if light.direction == RIGHT:
                    return [LightBeam(UP)]
            case "\\":
                if light.direction == UP:
                    return [LightBeam(LEFT)]
                if light.direction == LEFT:
                    return [LightBeam(UP)]
                if light.direction == DOWN:
                    return [LightBeam(RIGHT)]
                if light.direction == RIGHT:
                    return [LightBeam(DOWN)]


def create_tile(c: str):
    if c == ".":
        return Air(c)
    else:
        return Mirror(c)


class Maze:
    def __init__(self, lines) -> None:
        self.matrix: list[list[Tile]] = []
        for line in lines:
            self.matrix.append(list(map(create_tile, line)))
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])

    def trace_count_and_reset(self, original_beam: LightBeam, coords:tuple[int]):
        self.trace(original_beam, coords)
        energy = self.count_energised()
        for line in self.matrix:
            for tile in line:
                tile.reset_energy()
        return energy

    def trace(self, original_beam: LightBeam, coords: tuple[int]):
        beams = [original_beam]
        while len(beams) == 1:
            beam = beams[0]
            if not 0 <= coords[0] < self.width or not 0 <= coords[1] < self.height:
                return
            tile: Tile = self.matrix[coords[1]][coords[0]]
            if tile.is_energised_in_direction(beam.direction):
                return
            tile.energise_in_direction(beam.direction)
            beams = tile.route(beam)
            if len(beams) == 1:
                beam = beams[0]
                coords = (coords[0] + beam.direction[0], coords[1] + beams[0].direction[1])
        for beam in beams:
            new_coords = (coords[0] + beam.direction[0], coords[1] + beam.direction[1])
            self.trace(beam, new_coords)

    def count_energised(self):
        return sum(map(lambda line: sum(1 for c in line if c.is_energised()), self.matrix))

    def __str__(self) -> str:
        output = ""
        for line in self.matrix:
            output += "\n" + "".join(map(lambda x: str(x), line))
        return output


def task1(input):
    m = Maze(input)
    m.trace(LightBeam(RIGHT), (0, 0))
    return m.count_energised()


def task2(input):
    m = Maze(input)
    cases = []
    for x in range(m.width):
        cases.append({"beam": LightBeam(DOWN), "coords": (x, 0)})
        cases.append({"beam": LightBeam(UP), "coords": (x, m.height-1)})
    for y in range(m.height):
        cases.append({"beam": LightBeam(RIGHT), "coords": (0, y)})
        cases.append({"beam": LightBeam(LEFT), "coords": (m.width-1, y)})
    return max(map(lambda case: m.trace_count_and_reset(case["beam"], case["coords"]), cases))


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 16/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 16/input_test.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 46)

    def test2(self):
        self.assertEqual(task2(self.lines_test2), 51)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
