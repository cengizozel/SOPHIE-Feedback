import random
import re
import json

# function that returns text from a txt file
def get_text(filename):
    with open(filename, 'r') as f:
        return f.read()


# Take a txt file as input
# Remove "(", ")", "[", "]", and "|" from the lines
# Each sentence in the "sentence" varialbe should be capitalized
# Write the new text to a new file and call it "text_processed.txt"
def convert_text(filename, output_filename):
    with open(filename, 'r') as f:
        to_capitalize = [[" i ", " I "], ["i'm", "I'm"], ["i've", "I've"], ["sophie", "SOPHIE"]]
        lines = f.readlines()
        for i, line in enumerate(lines):
            # Removing last character (space) from name
            name = line.split(":")[0][:-1]
            sentence = line.split(":")[1]
            # Delete all the text between "[" and "]" using regex
            sentence = re.sub(r'\[.*?\]', '', sentence)
            # Make all letters lowercase
            sentence = sentence.lower()
            for char in ["(", ")", "|"]:
                if char in sentence:
                    sentence = sentence.replace(char, "")
            # Remove all spaces in the beginning of the sentence
            while sentence.startswith(" "):
                sentence = sentence.lstrip()
            # Remove all spaces before punctuation
            for rem in [" .", " ,", " !", " ?", " ;", " :", " -"]:
                if rem in sentence:
                    sentence = sentence.replace(rem, rem[1:].upper())
            # Split sentence by ".", "!", and "?"
            sentence_list = re.split(r'(?<=[.!?]) +', sentence)
            # Capitalize first letter of each sentence
            for j, s in enumerate(sentence_list):
                sentence_list[j] = s[0].upper() + s[1:]
            # Join the sentences back together
            sentence = " ".join(sentence_list)
            for tc in to_capitalize:
                sentence = sentence.replace(tc[0], tc[1])
            lines[i] = name + ": " + sentence
    with open(output_filename, 'w') as f:
        f.writelines(lines)

# function that takes a txt filename as input and returns a list of lines in the file without the newline character
def get_dialogue(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def get_inference(text, inference, obligations, use_model=False):
    # Inference is the file that contains the inference results
    # Text is the file that contains the conversation log
    with open(text, 'r') as f:
        text_lines = f.readlines()
    with open(inference, 'r') as f:
        inf_lines = f.readlines()
    with open(obligations, 'r') as f:
        obligations_lines = f.readlines()
    three_es, missed_opportunities = [], []

    for i, line in enumerate(inf_lines):
        if "EMPOWERING" in line:
            three_es.append(["Empowering", i, text_lines[i-1], text_lines[i]])
        if "EXPLICIT" in line:
            three_es.append(["Explicit", i, text_lines[i-1], text_lines[i]])
        if "EMPATHETIC" in line:
            three_es.append(["Empathy", i, text_lines[i-1], text_lines[i]])

        # Sort three_es by the first element (inference type)
        # The order should be Empowering, Explicit, Empathy
        order = {"Empathy": 0, "Explicit": 1, "Empowering": 2}
        three_es = sorted(three_es, key=lambda x: order[x[0]])

    for i, line in enumerate(obligations_lines):
        if i < len(obligations_lines)-1:
            if "EMPOWERING" in line:
                if "NIL" in inf_lines[i+1]:
                    missed_opportunities.append([text_lines[i], text_lines[i+1], "Empowering"])
            elif "EXPLICIT" in line:
                if "NIL" in inf_lines[i+1]:
                    missed_opportunities.append([text_lines[i], text_lines[i+1], "Explicit"])
            elif "EMPATHETIC" in line:
                if "NIL" in inf_lines[i+1]:
                    missed_opportunities.append([text_lines[i], text_lines[i+1], "Empathy"])

    # remove items from missed_opportunities where element[1] contains a question mark
    missed_opportunities = [x for x in missed_opportunities if "?" not in x[1]]
    missed_opportunities = sorted(missed_opportunities, key=lambda x: order[x[2]])

    return three_es, missed_opportunities
