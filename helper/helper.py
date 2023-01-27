import random

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

def get_inference(inference, text):
    # Inference is the file that contains the inference results
    # Text is the file that contains the conversation log
    with open(text, 'r') as f:
        text_lines = f.readlines()
    empower, explicit, empathy, missed_opportunities = "", "", "", []
    # Return a list of the line numbers where the line is not "NIL"
    with open(inference, 'r') as f:
        inf_lines = f.readlines()
        for i, line in enumerate(inf_lines):
            if "EMPOWERING" in line:
                empower = text_lines[i].split(":")[1]
            elif "EXPLICIT" in line:
                explicit = text_lines[i].split(":")[1]
            elif "EMPATHETIC" in line:
                empathy = text_lines[i].split(":")[1]
            elif "NIL" in line and not "Sophie" in text_lines[i]:
                # Make sure we don't go out of bounds
                if i+8 < len(inf_lines):
                    if "NIL" in inf_lines[i+2] and "NIL" in inf_lines[i+4] and "NIL" in inf_lines[i+6] and "NIL" in inf_lines[i+8]:
                        missed_opportunities.append(text_lines[i+8].split(":")[1])

    return empower, explicit, empathy, missed_opportunities
