import re

NAME_AGENT = "Sophie Hallman"
NAME_USER = "Doctor"

# function that returns text from a txt file
def get_text(filename):
    with open(filename, 'r') as f:
        return f.read()
    

# function to take the union of two lists
def list_union(l1, l2):
    return list(set(l1).union(set(l2)))


# Take a txt file as input
# Remove "(", ")", "[", "]", and "|" from the lines
# Each sentence in the "sentence" variable should be capitalized
# Write the new text to a new file and call it "text_processed.txt"
def convert_text(filename, output_filename):
    with open(filename, 'r') as f:
        to_capitalize = [[" i ", " I "], ["i'm", "I'm"], ["i've", "I've"], ["sophie", "SOPHIE"]]
        lines = f.readlines()
        for i, line in enumerate(lines):
            # Split off agent
            parts = line.split(':')
            agent = parts[0]
            sentence = parts[1]
            # Set name based on agent
            name = NAME_AGENT if agent.strip() == '^me' else NAME_USER
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
            # Capitalize specific words
            for tc in to_capitalize:
                sentence = sentence.replace(tc[0], tc[1])
            # Add agent name
            lines[i] = name + ": " + sentence
    with open(output_filename, 'w') as f:
        f.writelines(lines)


# function that takes a txt filename as input and returns a list of lines in the file without the newline character
def get_dialogue(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def get_inference(text, inference, obligations):
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
        skills_inf.append([skill for skill in skill_enum if skill in inf_line])
        skills_obl.append([skill for skill in skill_enum if skill in obligation_line])

    explicit_word_limit = 400
    # Flag all turns in which one of the three E's was used
    for i, skills in enumerate(skills_inf):
        if not text_lines[i].startswith(NAME_AGENT): # and "Let's pause here for feedback on this conversation." not in text_lines[i] -> Sophie says this anyway
            if "empowering" in skills:
                three_es.append(["Empower", i, text_lines[i-1], text_lines[i]])
            if "explicit" in skills:
                print(f"Explicit line length {len(text_lines[i])}")
                three_es.append(["be Explicit", i, text_lines[i-1], text_lines[i]])
            if "empathetic" in skills:
                three_es.append(["Empathize", i, text_lines[i-1], text_lines[i]])

        # Sort three_es by the first element (inference type)
        # The order should be Empowering, Explicit, Empathy
        order = {"Empathize": 0, "be Explicit": 1, "Empower": 2}
        three_es = sorted(three_es, key=lambda x: order[x[0]])

    # print(f"All skills {skills_obl}")
    # print(f"Displayed {skills_inf}")

    # Flag all clinician turns in which there was a missed obligation to use one of the three E's
    for i, skills in enumerate(skills_obl):
        if i < len(obligations_lines)-1:
            if not text_lines[i+1].startswith(NAME_AGENT):
                # print(f"Checking {skills_inf[i+1]}")
                # print("explicit" in skills_inf[i+1])
                # print(skills_inf[i+1] == ['explicit'])
                if "empowering" in skills:
                    if not skills_inf[i+1] or skills_inf[i+1] == ['explicit']: # If it's explicit, it still is a missed opportunity
                        print(f"empowering check: skills_inf[i+1] is {skills_inf[i+1]}")
                        missed_opportunities.append([text_lines[i], text_lines[i+1], "Empower"])
                elif "explicit" in skills:
                    if not skills_inf[i+1]:
                        print(f"explicit check: skills_inf[i+1] is {skills_inf[i+1]}")
                        missed_opportunities.append([text_lines[i], text_lines[i+1], "be Explicit"])
                    elif skills_inf[i+1] == ['explicit'] and len(text_lines[i+1]) > explicit_word_limit:
                        missed_opportunities.append([text_lines[i], text_lines[i+1], "be Explicit"])
                # else:
                #     print("Lecturing detected")
                #     missed_opportunities.append([text_lines[i-1], text_lines[i], "be Explicit"])
                elif "empathetic" in skills:
                    if not skills_inf[i+1] or skills_inf[i+1] == ['explicit']:
                        print(f"empathetic check: skills_inf[i+1] is {skills_inf[i+1]}")
                        missed_opportunities.append([text_lines[i], text_lines[i+1], "Empathize"])

    # remove items from missed_opportunities where element[1] contains a question mark
    missed_opportunities = [x for x in missed_opportunities if "?" not in x[1]]
    missed_opportunities = sorted(missed_opportunities, key=lambda x: order[x[2]])

    # TODO finalize what will be shown for the user's master's module
    # TODO finalize what will be shown for the user's master's module
    # TODO finalize what will be shown for the user's master's module
   

    return three_es, missed_opportunities
