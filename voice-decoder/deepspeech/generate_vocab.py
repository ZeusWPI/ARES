import random


nato = {'alpha': 'A', 'bravo': 'B', 'charlie': 'C', 'delta': 'D', 'echo': 'E', 'foxtrot': 'F', 'golf': 'G', 'hotel': 'H', 'india': 'I', 'juliet': 'J', 'kilo': 'K', 'lima': 'L', 'mike': 'M', 'november': 'N', 'oscar': 'O', 'papa': 'P', 'quebec': 'Q', 'romeo': 'R', 'sierra': 'S', 'tango': 'T', 'uniform': 'U', 'victor': 'V', 'whiskey': 'W', 'exray': 'X', 'yankee': 'Y', 'zulu': 'Z'}


nato = list(nato.keys())

numbers = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

def generate_callsign():
    return ' '.join(random.choices(nato + numbers, weights=[4]*26 + [1]*10, k=6))


def generate_authorization():
    auth = random.choice(['authenticate', 'authentication code'])
    code = ' '.join(random.choices(numbers, k=6))
    return f'{auth} {code}'


def generate_door():
    subaction = random.choice(['close', 'open'])
    return f'door {subaction}'

def generate_command():
    action = random.choice([generate_door])
    return f'command {action()}'

def generate_sentence():
    return f'this is {generate_callsign()} {generate_authorization()} {generate_command()}'


samples = set()
while len(samples) < 100_000:
    samples.add(generate_sentence())

with open('vocab.txt', 'w') as outfile:
    for sample in samples:
        print(sample, file=outfile)
