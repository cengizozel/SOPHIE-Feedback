# function that returns text from a txt file
def get_text(filename):
    with open(filename, 'r') as f:
        return f.read()

# function that takes a txt filename as input and returns a list of lines in the file without the newline character
def get_dialogue(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]