import copy
import unittest
import numpy as np
import regex


def main():
    with open("Day 10/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


DIRECTIONS = {
    'UP': np.array([0, -1]),
    'DOWN': np.array([0, 1]),
    'LEFT': np.array([-1, 0]),
    'RIGHT': np.array([1, 0])
}


def opposite_direction(direction):
    return np.array([direction[0] * -1, direction[1] * -1])


class Pipe:
    def __init__(self, character) -> None:
        self.character = character

    def connects(self, direction):
        if (direction == DIRECTIONS["LEFT"]).all():
            return self.character in ('-7J')
        if (direction == DIRECTIONS["RIGHT"]).all():
            return self.character in ('-FL')
        if (direction == DIRECTIONS["UP"]).all():
            return self.character in ('|LJ')
        if (direction == DIRECTIONS["DOWN"]).all():
            return self.character in ('|7F')
        return False

    def traverse(self, origin_direction):
        return next(filter(lambda d: self.connects(d) and not (d == origin_direction).all(), DIRECTIONS.values()))


def is_np_array_in_list(array, list_to_check_in):
    return any(map(lambda member: (member == array).all(), list_to_check_in))


class Pipes:
    def __init__(self, lines):
        self.network = []
        for line in lines:
            self.network.append(list([Pipe(c) for c in line]))

    def start_location(self):
        for index_y, line in enumerate(self.network):
            for index_x, pipe in enumerate(line):
                if pipe.character == "S":
                    return np.array([index_x, index_y])

    def pipe_at(self, coords: np.array):
        return self.network[coords[1]][coords[0]]

    def loop_length(self):
        start = self.start_location()
        direction = next(filter(lambda d: self.pipe_at(
            start + d).connects(opposite_direction(d)), DIRECTIONS.values()))
        current_pipe_coords = start + direction
        count = 1
        while self.pipe_at(current_pipe_coords).character != "S":
            direction = self.pipe_at(current_pipe_coords).traverse(
                opposite_direction(direction))
            current_pipe_coords += direction
            count += 1
        return count

    def cleaned_up(self):
        start = self.start_location()
        first_direction = next(filter(lambda d: self.pipe_at(
            start + d).connects(opposite_direction(d)), DIRECTIONS.values()))
        direction = copy.deepcopy(first_direction)
        current_pipe_coords = start + direction

        main_loop_coords = set([tuple(current_pipe_coords)])
        while self.pipe_at(current_pipe_coords).character != "S":
            direction = self.pipe_at(current_pipe_coords).traverse(
                opposite_direction(direction))
            current_pipe_coords += direction
            main_loop_coords.add(tuple(current_pipe_coords))
        new_network = []
        for index_y, line in enumerate(self.network):
            new_network_line = []
            for index_x, pipe in enumerate(line):
                if (index_x, index_y) in main_loop_coords:
                    new_network_line.append(copy.deepcopy(pipe))
                else:
                    new_network_line.append(Pipe("."))
            new_network.append(new_network_line)

        s_directions = (first_direction, opposite_direction(direction))
        if is_np_array_in_list(DIRECTIONS["UP"], s_directions) and is_np_array_in_list(DIRECTIONS["LEFT"], s_directions):
            S_replacement = "J"
        if is_np_array_in_list(DIRECTIONS["UP"], s_directions) and is_np_array_in_list(DIRECTIONS["RIGHT"], s_directions):
            S_replacement = "L"
        if is_np_array_in_list(DIRECTIONS["DOWN"], s_directions) and is_np_array_in_list(DIRECTIONS["LEFT"], s_directions):
            S_replacement = "7"
        if is_np_array_in_list(DIRECTIONS["DOWN"], s_directions) and is_np_array_in_list(DIRECTIONS["RIGHT"], s_directions):
            S_replacement = "F"
        if is_np_array_in_list(DIRECTIONS["UP"], s_directions) and is_np_array_in_list(DIRECTIONS["DOWN"], s_directions):
            S_replacement = "|"
        if is_np_array_in_list(DIRECTIONS["LEFT"], s_directions) and is_np_array_in_list(DIRECTIONS["RIGHT"], s_directions):
            S_replacement = "-"
        assert (S_replacement is not None)
        for line in new_network:
            for pipe in line:
                if pipe.character == "S":
                    pipe.character = S_replacement
        return new_network

    def sequence_to_left(self, coords, network):
        return "".join(map(lambda p: p.character, network[coords[1]][:coords[0]]))

    def number_of_crossings(self, sequence):
        sequence = regex.sub(r'F-*J', '|', sequence)
        sequence = regex.sub(r'L-*7', '|', sequence)
        return sum([1 for c in sequence if c == "|"])

    def count_enclosed(self):
        clean_network = self.cleaned_up()
        for line in clean_network:
            print("".join(map(lambda p: p.character, line)))
        count = 0
        for index_y, line in enumerate(clean_network):
            for index_x, pipe in enumerate(line):
                if pipe.character == "." and self.number_of_crossings(self.sequence_to_left(np.array([index_x, index_y]), clean_network)) % 2 == 1:
                    count += 1
        return count


def task1(input):
    return int(Pipes(input).loop_length()/2)


def task2(input):
    return Pipes(input).count_enclosed()


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 10/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 10/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test_pipe_connects(self):
        self.assertEqual(Pipe("J").connects(DIRECTIONS["LEFT"]), True)
        self.assertEqual(Pipe("J").connects(DIRECTIONS["RIGHT"]), False)

    def test(self):
        self.assertEqual(task1(self.lines_test), 8)

    def test2(self):
        self.assertEqual(task2(self.lines_test2), 10)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
