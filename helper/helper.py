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
        to_capitalize = [[" i ", " I "], ["i'm", "I'm"], ["sophie", "SOPHIE"]]
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
    highlights = [0, 0, 0]
    # Return a list of the line numbers where the line is not "NIL"
    with open(inference, 'r') as f:
        inf_lines = f.readlines()
        for i, line in enumerate(inf_lines):
            if "EMPOWERING" in line:
                empower = text_lines[i].split(":")[1]
                highlights[0] = i
            elif "EXPLICIT" in line:
                explicit = text_lines[i].split(":")[1]
                highlights[1] = i
            elif "EMPATHETIC" in line:
                empathy = text_lines[i].split(":")[1]
                highlights[2] = i
            elif "NIL" in line and not "Sophie" in text_lines[i]:
                # Make sure we don't go out of bounds
                if i+8 < len(inf_lines):
                    if "NIL" in inf_lines[i+2] and "NIL" in inf_lines[i+4] and "NIL" in inf_lines[i+6] and "NIL" in inf_lines[i+8]:
                        missed_opportunities.append(
                            text_lines[i+8].split(":")[1])

    return empower, explicit, empathy, highlights, missed_opportunities


def create_json():
    data = {
        "transcript": {
            "empower": [],
            "explicit": [],
            "emapthy": []
        },
        "empower": {
            "questions_asked": 5,
            "open_ended": 6,
            "turn_taking": []
        },
        "explicit": {
            "hedge_word_cloud": ["a", "b", "c"],
            "hedge_words": [19, 158],
            "speaking_rate": 40,
            "reading_level": 5
        },
        "empathize": {
            "personal_pronouns": [29, 158],
            "empathy_word_cloud": ["a", "b", "c"],
            "average_empathy": 50
        }
    }

    return json.dumps(data)
