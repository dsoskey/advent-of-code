from functools import reduce, cmp_to_key


def collect(prev, _next):
    if prev.get(_next) is None:
        prev[_next] = 0
    prev[_next] += 1
    return prev


class Hand:
    hand_size = 5
    card_strengths = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "J": 10,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
    }
    joker_strengths = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
        "J": 0,

    }

    def __init__(self, bet_line: str, use_jokers=False):
        raw_hand, raw_bid = bet_line.split(" ")
        assert len(raw_hand) == Hand.hand_size, "invalid hand size"
        self.raw = raw_hand
        self.parsed = self.parse_joker_hand() if use_jokers else self.parse_normal_hand()
        self.bid = int(raw_bid)

    def parse_hand_rank(self):
        num_unique = len(self.parsed.keys())
        quantities = list(self.parsed.values())

        if num_unique == 1 and quantities.count(5):
            return 7
        elif num_unique == 2:
            return 6 if quantities.count(4) else 5
        elif num_unique == 3:
            return 4 if quantities.count(3) else 3
        elif num_unique == 4 and quantities.count(2):
            return 2
        else:
            return 1

    def parse_normal_hand(self):
        lookup: dict = reduce(collect, [ch for ch in self.raw], {})
        return lookup

    def parse_joker_hand(self):
        lookup: dict = reduce(collect, [ch for ch in self.raw], {})
        joker_count = lookup.get("J", 0)
        if joker_count in range(1, Hand.hand_size):
            del lookup["J"]
            strongest = max(lookup.items(), key=cmp_to_key(Hand.jokerable))
            lookup[strongest[0]] += joker_count
        return lookup

    @staticmethod
    def jokerable(left, right):
        if left[1] == right[1]:
            return Hand.card_strengths.get(left[0], 0) - Hand.card_strengths.get(right[0], 0)
        return left[1] - right[1]

    @staticmethod
    def winner(card_strengths):
        def inner(left, right):
            left_rank = left.parse_hand_rank()
            right_rank = right.parse_hand_rank()
            if left_rank == right_rank:
                for i in range(Hand.hand_size):
                    l_strength = card_strengths.get(left.raw[i], 0)
                    r_strength = card_strengths.get(right.raw[i], 0)
                    if l_strength == r_strength:
                        continue
                    return l_strength - r_strength
                return 0
            return left_rank - right_rank

        return inner


def get_total_winnings(raw_game: str, use_jokers=False):
    card_strengths = Hand.joker_strengths if use_jokers else Hand.card_strengths
    hands = list(map(lambda it: Hand(it, use_jokers), raw_game.splitlines()))
    by_rank = sorted(hands, key=cmp_to_key(Hand.winner(card_strengths)))
    points = [(i + 1) * hand.bid for i, hand in enumerate(by_rank)]
    return reduce(int.__add__, points)


if __name__ == "__main__":
    with open("./input") as file:
        text = file.read()
        print(f"total winnings: {get_total_winnings(text, False)}")
        print(f"total winnings with Jokers: {get_total_winnings(text, True)}")
