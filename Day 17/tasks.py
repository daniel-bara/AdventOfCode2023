from dataclasses import dataclass
import math
import time
import unittest


def main():
    with open("Day 17/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


LEFT = (-1, 0)
UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
DIRECTIONS = (LEFT, UP, RIGHT, DOWN)


def opposite_direction(direction):
    return (direction[0]*-1, direction[1]*-1)


@dataclass
class State:
    cost: int
    coords: tuple
    step_no: int
    direction: tuple[int]


@dataclass
class Tile:
    heat_loss: int
    explored = False


def step_in_direction(coords, direction):
    return (coords[0] + direction[0], coords[1] + direction[1])


class Maze:
    def __init__(self, lines, minimum_steps = None, maximum_steps = None) -> None:
        self.matrix = []

        if minimum_steps is None:
            self.minimum_steps = 0
        else:
            self.minimum_steps = minimum_steps
        self.maximum_steps = maximum_steps
        for index_y, line in enumerate(lines):
            tile_line = []
            for index_x, char in enumerate(line):
                tile_line.append(Tile(int(char)))
            self.matrix.append(tile_line)
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])
        self.min_cost_per_tile = {}  # {(0, 0, 0, 1: 0)} # not step count, but direction

    def next_steps(self, step: State):
        self.matrix_safe_get(step.coords, Tile(1000)).explored = True
        if step.cost >= self.min_cost_per_tile.get((*step.coords, *step.direction, step.step_no), math.inf):
            return
        self.min_cost_per_tile[(*step.coords, *step.direction, step.step_no)] = step.cost
        for direction in DIRECTIONS:
            new_step_no = step.step_no + 1
            if step.direction == opposite_direction(direction):  # do not go backwards
                continue
            elif step.direction == direction:
                if new_step_no >= self.maximum_steps:
                    continue
                else:
                    new_coords = step_in_direction(step.coords, direction)
                    new_cost = step.cost + self.matrix_safe_get(new_coords, Tile(1000)).heat_loss
                    if new_cost < self.min_cost_per_tile.get((*new_coords, direction, new_step_no), math.inf):
                        yield State(new_cost, new_coords, new_step_no, direction)
            else:
                if new_step_no < self.minimum_steps:
                    continue
                new_coords = step_in_direction(step.coords, direction)
                new_cost = step.cost + self.matrix_safe_get(new_coords, Tile(1000)).heat_loss
                new_step_no = 0
                if new_cost < self.min_cost_per_tile.get((*new_coords, direction, new_step_no), math.inf):
                    yield State(new_cost, new_coords, new_step_no, direction)

    def check_cost(self, coords, return_steps=False):
        cost_and_dir = min(
            map(lambda dir: min(map(lambda step_no:
                                    {"cost": self.min_cost_per_tile.get(
                                        (*coords, *dir, step_no), math.inf), "direction": dir},
                                    range(self.minimum_steps-1, self.maximum_steps)), key=lambda dict: dict["cost"]),
                DIRECTIONS),
            key=lambda dict: dict["cost"])
        if return_steps:
            return cost_and_dir
        return cost_and_dir["cost"]

    def cost_minimum_search(self, destination_coords, stopwatch = 0):
        states = {0: [State(0, (0, 0), 0, DOWN), State(0, (0, 0), 0, RIGHT)]}
        progress = 0
        cost_progress = 0
        while self.check_cost(destination_coords) == math.inf:
            for next_state in self.next_steps(states[cost_progress].pop(0)):
                if next_state.cost not in states:
                    states[next_state.cost] = []
                states[next_state.cost].append(next_state)
            
            while len(states.get(cost_progress, [])) == 0:
                    cost_progress += 1
            best_state = states[cost_progress][0]
            manhattan_distance_covered = best_state.coords[0] + best_state.coords[1]
            if manhattan_distance_covered > progress:
                progress = manhattan_distance_covered
                # print(progress)
        return self.check_cost(destination_coords)

    def matrix_safe_get(self, coords, default) -> Tile:
        if 0 <= coords[0] < self.width and 0 <= coords[1] < self.height:
            return self.matrix[coords[1]][coords[0]]
        return default

    def backtrack(self, coords):
        cost, steps = self.check_cost(coords, return_steps=True).values()
        backtrack_dir = None
        while coords != (0, 1) and coords != (1, 0):
            for direction in DIRECTIONS:
                new_coords = (coords[0]+direction[0], coords[1] + direction[1])
                if steps > 0:
                    if self.min_cost_per_tile.get((*new_coords, steps-1), math.inf) == cost - self.matrix_safe_get(coords, math.inf).heat_loss:
                        coords = new_coords
                        backtrack_dir = direction
                        cost -= self.matrix_safe_get(coords, math.inf).heat_loss
                        steps -= 1
                        print(coords)
                else:
                    if direction == backtrack_dir:
                        continue
                    new_step, new_cost = self.check_cost(new_coords, return_steps=True)
                    if new_cost == cost - self.matrix_safe_get(coords, math.inf).heat_loss:
                        coords = new_coords
                        backtrack_dir = direction
                        cost -= self.matrix_safe_get(coords, math.inf).heat_loss
                        steps = new_step
                        print(coords)

    def __str__(self) -> str:
        output = ""
        for index_y, line in enumerate(self.matrix):
            output += "\n"
            for index_x, tile in enumerate(line):
                if tile.explored:
                    output += f"{str(self.check_cost((index_x, index_y))):3}"
                else:
                    output += f"{str(tile.heat_loss):3}"
        return output


def task1(input):
    m = Maze(input, maximum_steps=3)
    cost = m.cost_minimum_search((m.width-1, m.height-1))
    return cost


def task2(input):
    m = Maze(input, minimum_steps=4, maximum_steps=10)
    cost = m.cost_minimum_search((m.width-1, m.height-1))
    return cost


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 17/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 17/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test_cost(self):
        m = Maze(self.lines_test, maximum_steps=3)
        self.assertEqual(m.cost_minimum_search((1, 0)), 4)
        m = Maze(self.lines_test, maximum_steps=3)
        self.assertEqual(m.cost_minimum_search((4, 0)), 14)
        m = Maze(self.lines_test, maximum_steps=3)
        self.assertEqual(m.cost_minimum_search((5, 0)), 17)
        m = Maze(self.lines_test, maximum_steps=3)
        self.assertEqual(m.cost_minimum_search((8, 0)), 29)

    def test(self):
        self.assertEqual(task1(self.lines_test), 102)

    def test2(self):
        self.assertEqual(task2(self.lines_test2), 71)
        self.assertEqual(task2(self.lines_test), 94)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
