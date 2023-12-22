import math
import unittest

import regex


def main():
    with open("Day 19/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    # print(f"Task 2: {task2(lines)}")


class Rule:
    def __init__(self, text) -> None:
        conditional = regex.match(r'(?P<prop>\w+)(?P<relation><|>)(?P<threshold>\d+):(?P<destination>\w+)', text)
        self.unconditional = False
        if not conditional:
            unconditional = regex.match(r'(?P<destination>\w+)', text)
            self.destination = unconditional.group('destination')
            self.unconditional = True
            return

        self.prop = conditional.group('prop')
        self.threshold = int(conditional.group('threshold'))
        self.relation = conditional.group('relation')
        self.destination = conditional.group('destination')

    def process(self, part: dict):
        if self.unconditional:
            return self.destination
        if self.relation == "<" and part[self.prop] < self.threshold:
            return self.destination
        if self.relation == ">" and part[self.prop] > self.threshold:
            return self.destination
        return False


class Workflow:
    def __init__(self, line) -> None:
        m = regex.match(r'(?P<name>\w+)\{(?P<rules>.+)\}', line)
        self.name = m.group('name')
        rules_str = m.group('rules')
        self.rules = list(map(Rule, rules_str.split(",")))

    def process(self, part):
        for rule in self.rules:
            if rule.process(part) != False:
                return rule.process(part)

    def process_1d(self, i: int, prop):
        for rule in self.rules:
            if not rule.unconditional and rule.prop != prop:
                continue
            if rule.process({prop: i}) != False:
                return rule.process({prop: i})


class Part:
    def __init__(self, line) -> None:
        m = regex.match(r'\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)\}', line)
        self.lookup = {"x": int(m.group('x')),
                       "m": int(m.group('m')),
                       "a": int(m.group('a')),
                       "s": int(m.group('s'))}

    def __getitem__(self, __key):
        return self.lookup[__key]

    def get_sum(self):
        return sum(self.lookup.values())


def task1(input):
    workflows_str, parts_str = "\n".join(input).split("\n\n")
    workflows_lines = list(workflows_str.split("\n"))
    parts_lines = list(parts_str.split("\n"))
    workflows = list(map(Workflow, workflows_lines))
    workflows_dict = dict(zip(map(lambda w: w.name, workflows), workflows))
    parts = list(map(Part, parts_lines))
    counter = 0
    for part in parts:
        workflow = "in"
        while workflow not in ("A", "R"):
            workflow = workflows_dict[workflow].process(part)
        if workflow == "A":
            counter += part.get_sum()

    return counter


def task2(input):
    pass


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 19/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 19114)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 167409079868000)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
