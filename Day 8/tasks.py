import unittest
from dataclasses import dataclass
import regex
import math


def main():
    with open("Day 8/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


@dataclass
class Node:
    id: str
    left_id: str
    right_id: str


def sequence_iterator(sequence):
    while True:
        for character in sequence:
            yield character


def find_node_by_id(id, node_list: list[Node]) -> Node:
    return next(filter(lambda n: n.id == id, node_list))


def task1(input):
    nodes: list(Node) = []
    sequence = sequence_iterator(input[0])
    for line in input[2:]:
        nodes.append(Node(
            regex.match(r'\w+', line).group(0),
            regex.search(r'(?:\()(\w+)', line).group(1),
            regex.search(r'(\w+)(?:\))', line).group(1)
        ))
    current_node = find_node_by_id("AAA", nodes)
    count = 0
    while current_node.id != 'ZZZ':
        if next(sequence) == "L":
            current_node = find_node_by_id(current_node.left_id, nodes)
        else:
            current_node = find_node_by_id(current_node.right_id, nodes)
        count += 1
    return count


def task2(input):
    nodes: list(Node) = []
    sequence = sequence_iterator(input[0])
    for line in input[2:]:
        nodes.append(Node(
            regex.match(r'\w+', line).group(0),
            regex.search(r'(?:\()(\w+)', line).group(1),
            regex.search(r'(\w+)(?:\))', line).group(1)
        ))
    current_nodes = list(filter(lambda n: n.id[-1] == "A", nodes))
    loop_lengths = {}
    count = 0
    while not all(map(lambda n: n.id[-1] == "Z", current_nodes)):
        if next(sequence) == "L":
            for i in range(len(current_nodes)):
                current_nodes[i] = find_node_by_id(current_nodes[i].left_id, nodes)
        else:
            for i in range(len(current_nodes)):
                current_nodes[i] = find_node_by_id(current_nodes[i].right_id, nodes)
        count += 1
        for i in range(len(current_nodes)):
            if  current_nodes[i].id[-1] == "Z":
                print(f"Ghost {i} finished at {count} {current_nodes[i].id}")
                if not loop_lengths.get(i, None):
                    loop_lengths[i] = count
                if len(loop_lengths) == len(current_nodes):
                    return math.lcm(*loop_lengths.values()) # I don't know why this works but it does
    return count


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 8/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 8/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))
        with open("Day 8/input_test3.txt") as file:
            self.lines_test3 = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 2)
        self.assertEqual(task1(self.lines_test2), 6)

    def test2(self):
        self.assertEqual(task2(self.lines_test3), 6)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
