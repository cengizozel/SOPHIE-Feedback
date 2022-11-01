from cv2 import IMWRITE_PAM_FORMAT_GRAYSCALE


import random

from numpy import empty

# function that returns text from a txt file
def get_text(filename):
    with open(filename, 'r') as f:
        return f.read()

# function that takes a txt filename as input and returns a list of lines in the file without the newline character
def get_dialogue(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

# function that takes a txt filename and a number as input and returns n random lines from the text and returns them as a list
def random_empathy(filename, n):
    with open(filename, 'r') as f:
        return random.sample(f.readlines(), n)