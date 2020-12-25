import re
import string
import sys
import json
import os

import requests
from pyotp.totp import TOTP

nato = {'alpha': 'A', 'bravo': 'B', 'charlie': 'C', 'delta': 'D', 'echo': 'E', 'foxtrot': 'F', 'golf': 'G', 'hotel': 'H', 'india': 'I', 'juliet': 'J', 'kilo': 'K', 'lima': 'L', 'mike': 'M', 'november': 'N', 'oscar': 'O', 'papa': 'P', 'quebec': 'Q', 'romeo': 'R', 'sierra': 'S', 'tango': 'T', 'uniform': 'U', 'victor': 'V', 'whiskey': 'W', 'exray': 'X', 'yankee': 'Y', 'zulu': 'Z'}
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


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def similar_enough(received, actual):
    '''Check if two strings are similar enough for authentication to allow access.
    >>> similar_enough('123456', '123456')
    True
    >>> similar_enough('12345', '123456')
    True
    >>> similar_enough('12345_', '123456')
    True
    '''
    return levenshteinDistance(received, actual) <= 1


def translate_best_effort(word, wordlist_from, wordlist_to, placeholder='_'):
    try:
        idx = wordlist_from.index(word)
        return wordlist_to[idx]
    except ValueError:
        return placeholder


def callsign_translate(callsign_words):
    '''Translates from words into callsign
    >>> callsign_translate('alpha zero one charlie')
    'A01C'
    '''
    words = callsign_words.split(' ')
    wordlist_from = numbers + list(nato.keys())
    wordlist_to = list(str(i) for i in range(10)) + list(string.ascii_uppercase)
    return ''.join(translate_best_effort(word, wordlist_from, wordlist_to) for word in words)


def authentication_code_translate(authentication_code_words):
    '''Translates from words into authentication code
    >>> authentication_code_translate('zero five three six nine eight')
    '053698'
    >>> authentication_code_translate('zero BUZZ three six nine eight')
    '0_3698'
    '''
    words = authentication_code_words.split(' ')
    wordlist_from = numbers
    wordlist_to = list(str(i) for i in range(10))
    return ''.join(translate_best_effort(word, wordlist_from, wordlist_to) for word in words)


def validate_sentence(s, actual_authentication_code):
    '''Parses a sentence and extracts command
    >>> validate_sentence('this is alpha six zero zulu five authentication code one two three four five six command door close', '123456')
    ('A60Z5', 'close')
    '''
    words = s.split(' ')
    command = None
    callsign = None
    if words[-1] not in ('open', 'close'):
        raise ValueError('Unknown command')
    command = words[-1]
    split_auth = re.split(' authentication code | authenticate ', s)
    if len(split_auth) < 2:
        raise ValueError('Could not split authentication part')
    if len(split_auth) > 2:
        raise ValueError('Too many authentication parts')
    callsign_part, auth_command_part = split_auth
    receieved_authentication_code = auth_command_part
    if ' command ' in auth_command_part:
        receieved_authentication_code = auth_command_part.split(' command ')[0]
    callsign_part = re.sub('(this|is) ', '', callsign_part)
    callsign = callsign_translate(callsign_part)
    if similar_enough(authentication_code_translate(receieved_authentication_code), actual_authentication_code):
        return callsign, command
    return callsign, None


if __name__ == '__main__':
    assert len(sys.argv) > 3, "need text, filename and secretsdb"
    with open(sys.argv[3]) as secretsfile:
        secretsdb = json.load(secretsfile)

    # ${DATE}_${SRCCALL}_${SRCID}_${DSTCALL}_${DSTID}.wav
    metadata_parts = sys.argv[2].split('_')
    src_callsign = metadata_parts[1]

    if src_callsign not in secretsdb:
        print("NOT FOUND")
        sys.exit(1)

    t = TOTP(secretsdb[src_callsign], interval=120)

    interpreted_callsign, command = validate_sentence(sys.argv[1], t.now())
    door_url = os.environ.get('DOOR_URL', 'https://example.com/door?token=test')
    if command is not None:
        requests.post(f'{door_url}&user_name={src_callsign}&text={command}')
    else:
        print('invalid code or command')

