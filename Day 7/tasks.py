import unittest
from dataclasses import dataclass
from itertools import groupby
import regex


def main():
    with open("Day 7/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


class Hand:
    def __init__(self, hand: str) -> None:
        self.hand = hand
        self.card_group_sizes = list([len(list(cards))
                                     for key, cards in groupby(sorted(self.hand))])

    def card_strength(self, card: str):
        return regex.search(card, "23456789TJQKA").start()

    def hand_sort_key(self):
        strength = 0
        for i in range(len(self.hand)):
            strength += self.card_strength(
                self.hand[i]) * 15**(len(self.hand) - i)

        strength += self.type_strength() * 15 ** (len(self.hand) + 1)
        return strength

    def type_strength(self):
        if self.is_five_of_a_kind():
            return 6
        if self.is_four_of_a_kind():
            return 5
        if self.is_full_house():
            return 4
        if self.is_three_of_a_kind():
            return 3
        if self.is_two_pair():
            return 2
        if self.is_one_pair():
            return 1
        if self.is_high_card():
            return 0

    def is_five_of_a_kind(self):
        return sorted(self.card_group_sizes) == [5]

    def is_four_of_a_kind(self):
        return sorted(self.card_group_sizes) == [1, 4]

    def is_full_house(self):
        return sorted(self.card_group_sizes) == [2, 3]

    def is_three_of_a_kind(self):
        return sorted(self.card_group_sizes) == [1, 1, 3]

    def is_two_pair(self):
        return sorted(self.card_group_sizes) == [1, 2, 2]

    def is_one_pair(self):
        return sorted(self.card_group_sizes) == [1, 1, 1, 2]

    def is_high_card(self):
        return sorted(self.card_group_sizes) == [1, 1, 1, 1, 1]


class Hand2(Hand):
    def __init__(self, hand: str) -> None:
        self.hand = hand
        card_groups = []
        for key, group in groupby(sorted(self.hand)):
            card_groups.append([key, list(group)])

        self.card_group_sizes = list([len(list(cards))
                                     for key, cards in groupby(sorted(self.hand))])

        if "J" in map(lambda g: g[0], card_groups):
            if self.hand == "JJJJJ":
                return
            self.J_count = sum([1 for c in self.hand if c == "J"])
            card_that_J_represents = sorted(filter(
                lambda g: g[0] != "J", card_groups), key=lambda g: len(list(g[1])), reverse=True)[0][0]
            hand_jokers_replaced = self.hand.replace(
                "J", card_that_J_represents)
            self.card_group_sizes = list([len(list(cards))
                                          for key, cards in groupby(sorted(hand_jokers_replaced))])

    def card_strength(self, card: str):
        return regex.search(card, "J23456789TQKA").start()


@dataclass
class HandBid:
    hand: Hand
    bid: int


def task1(input):
    handbids = [HandBid(Hand(line.split(" ")[0]), int(
        line.split(" ")[1])) for line in input]
    winnings = 0
    for index, handbid in enumerate(sorted(handbids, key=lambda handbid: handbid.hand.hand_sort_key())):
        winnings += handbid.bid * (index+1)

    return winnings


def task2(input):
    handbids = [HandBid(Hand2(line.split(" ")[0]), int(
        line.split(" ")[1])) for line in input]
    winnings = 0
    for index, handbid in enumerate(sorted(handbids, key=lambda handbid: handbid.hand.hand_sort_key())):
        winnings += handbid.bid * (index+1)

    return winnings


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 7/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 6440)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 5905)

    def test_five_of_a_kind(self):
        self.assertEqual(Hand("AAAAA").is_five_of_a_kind(), True)
        self.assertEqual(Hand("AABAA").is_five_of_a_kind(), False)

    def test_four_of_a_kind(self):
        self.assertEqual(Hand("ABAAA").is_four_of_a_kind(), True)
        self.assertEqual(Hand("AAAAA").is_four_of_a_kind(), False)

    def test_full_house(self):
        self.assertEqual(Hand("21112").is_full_house(), True)
        self.assertEqual(Hand("21113").is_full_house(), False)

    def test_type_strength(self):
        self.assertEqual(Hand("32T3K").type_strength(), 1)

    def test_hand2_type_strength(self):
        self.assertEqual(Hand2("JJJJJ").type_strength(), 6)

    def test_hand2_jokers(self):
        self.assertEqual(Hand2("88J88").is_five_of_a_kind(), True)
        self.assertEqual(Hand2("68JJ8").is_four_of_a_kind(), True)
        self.assertEqual(Hand2("87JJ8").is_four_of_a_kind(), True)
        self.assertEqual(Hand2("4J8J3").is_three_of_a_kind(), True)
        self.assertEqual(Hand2("J4224").is_full_house(), True)
        self.assertEqual(Hand2("J412K").is_one_pair(), True)
        self.assertEqual(Hand2("J4J2K").is_three_of_a_kind(), True)
        self.assertEqual(Hand2("87JJJ").is_four_of_a_kind(), True)
        self.assertEqual(Hand2("JQJJJ").is_five_of_a_kind(), True)

    def test_task2_sorting(self):
        self.assertEqual(task2(["JKKK2 5", "QQQQ2 4"]), 13)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
