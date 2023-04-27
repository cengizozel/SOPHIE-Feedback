import random
import re
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# function that returns text from a txt file
def get_text(filename):
    with open(filename, 'r') as f:
        return f.read()
    

# function to classify skills given a text string
def classify_skills(sentence, classifier):
    skill_enum = ["empowering", "explicit", "empathetic"]
    skills = classifier(sentence)[0]
    skills = [skill[1] for skill in zip(skills, skill_enum) if skill[0]['score'] > 0.5]
    return skills


# function to take the union of two lists
def list_union(l1, l2):
    return list(set(l1).union(set(l2)))


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


def get_inference(text, inference, obligations, skill_classifier=None):
    # Inference is the file that contains the inference results
    # Text is the file that contains the conversation log
    with open(text, 'r') as f:
        text_lines = f.readlines()
    with open(inference, 'r') as f:
        inf_lines = f.readlines()
    with open(obligations, 'r') as f:
        obligations_lines = f.readlines()
    three_es, missed_opportunities = [], []

    # Preprocess inferences and obligations by extracting skills
    skills_inf, skills_obl = [], []
    skill_enum = ["empowering", "explicit", "empathetic"]
    for i, (inf_line, obligation_line) in enumerate(zip(inf_lines, obligations_lines)):
        skills_inf.append([skill for skill in skill_enum if skill.upper() in inf_line])
        skills_obl.append([skill for skill in skill_enum if skill.upper() in obligation_line])

    # Add any skills for each turn detected by classifier (if not present already)
    if skill_classifier:
        for i, _ in enumerate(skills_inf):
            skills = classify_skills(text_lines[i], skill_classifier)
            skills_inf[i] = list_union(skills, skills_inf[i])

    # Flag all turns in which one of the three E's was used
    for i, skills in enumerate(skills_inf):
        if "empowering" in skills:
            three_es.append(["Empowering", i, text_lines[i-1], text_lines[i]])
        if "explicit" in skills:
            three_es.append(["Explicit", i, text_lines[i-1], text_lines[i]])
        if "empathetic" in skills:
            three_es.append(["Empathy", i, text_lines[i-1], text_lines[i]])

        # Sort three_es by the first element (inference type)
        # The order should be Empowering, Explicit, Empathy
        order = {"Empathy": 0, "Explicit": 1, "Empowering": 2}
        three_es = sorted(three_es, key=lambda x: order[x[0]])

    # Flag all turns in which there was a missed obligation to use one of the three E's
    for i, skills in enumerate(skills_obl):
        if i < len(obligations_lines)-1:
            if "empowering" in skills:
                if not skills_inf[i+1]:
                    missed_opportunities.append([text_lines[i], text_lines[i+1], "Empowering"])
            elif "explicit" in skills:
                if not skills_inf[i+1]:
                    missed_opportunities.append([text_lines[i], text_lines[i+1], "Explicit"])
            elif "empathetic" in skills:
                if not skills_inf[i+1]:
                    missed_opportunities.append([text_lines[i], text_lines[i+1], "Empathy"])

    # remove items from missed_opportunities where element[1] contains a question mark
    missed_opportunities = [x for x in missed_opportunities if "?" not in x[1]]
    missed_opportunities = sorted(missed_opportunities, key=lambda x: order[x[2]])

    return three_es, missed_opportunities
