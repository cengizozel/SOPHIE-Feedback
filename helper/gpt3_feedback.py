import os
import openai
openai.api_key = ""  # UofR key

EEE = """
The MVP (Medical situation, Values, Plan) communication protocol defines how doctors should communicate information about serious illness to their patients. The protocol stand on 3 major skills from doctors named 3E's: Empower, Explicit, Empathize.

A. Empower
- Listen
- Ask first
- Calibrate

B. be Explicit
Share the facts
- Precisely
- Concisely

C. Empathize
Emotion
- Anticipate & Recognize
- Validate & Explore

Here are some examples of the 3E's in action.

Empower:
• I'd like to discuss some difficult information with you, okay?
• Before I share the details, it will help me to know what you understand about the disease.
• Given your medical situation, what matters most to you? What are you hoping for?
• Now that I understand your values, I'd like to offer a recommendation, okay?
• Does my recommendation make sense? What do you think? 

be Explicit:
• I'm afraid I have some bad news…
• The treatment isn't working, and another round of therapy probably 
• Let me see if I understand. You value … (ex. quality over length of life…OR…doing everything to live another day… OR…).
• Given what you've told me, I recommend that we…(ex. take resuscitation off the table, and treat your symptoms at home…OR…offer a time limited ventilator trial…OR…).
• OK, now let's complete 2 forms (HCP, POLST) to be sure your medical team knows and honors your wishes, okay?

Empathy:
• I can see this is hard to hear.
• I wish we had better options.
• I appreciate how much you want to be here for your family
• Yes, of course! Anyone would find this discussion difficult.
• It's a privilege to work with you. You've done a great job taking care of yourself, and your family.

Based on the MVP clinical communication protocol and 3E skillset, evaluate the following conversation between a clinician and a patient. Acknowledge where the clinician did right based on the 3E skillset. Provide detailed feedback if the clinician missed something and where they could do better. Be encouraging to the clinician, and help them improve their communication skill.

\"\"\"
[[conversation]]
\"\"\"

Write a brief but powerful feedback to the clinician in second person based on the MVP protocol:
"""


def get_feedback(transcript):
    global EEE
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=EEE.replace("[[conversation]]", transcript),
        temperature=0.73,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"].strip()
