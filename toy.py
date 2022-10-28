import random
import string

def random_string(count):
    all_strings = []
    for i in range(count):
        all_strings.append(''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    return all_strings