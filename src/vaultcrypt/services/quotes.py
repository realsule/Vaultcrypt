import random

QUOTES = [
    "Discipline beats motivation. Do it anyway.",
    "Small wins compound into empires.",
    "Protect your passwords the way you protect your goals.",
    "Consistency is your competitive advantage.",
    "Build quietly. Ship loudly."
]


def random_quote() -> str:
    return random.choice(QUOTES) # return a random motivational quote