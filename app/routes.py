from app import app
from flask import render_template, request
import openai
from transformers import GPT2Tokenizer
import os

# with open("OPENAI_API_KEY.txt", "r") as k:
#     openai.api_key = k.readline()
#     k.close()
openai.api_key = os.environ["OPENAI_API_KEY"]

extra_markers = ["AP", "TIP", "NOTE", "AP®"]
punctuation = [".", "!", "?"]


@app.route("/", methods=["GET", "POST"])
def home():
    notes = ""
    extra_notes = ""
    in_extra = False
    raw_notes = []

    input = None

    if request.method == "POST":
        input = request.form["text_in"]
        lines = [line.strip() for line in input.split("\n") if len(line) > 1]  # TODO: failure point
        for curline in lines:
            not_sentence = curline[-1] not in punctuation
            is_short = len(curline.split()) < 10
            caps = [word[0].isupper() for word in curline.split()]
            is_heading = caps.count(True)/len(caps) > 0.5
            extra = curline.split()[0] in extra_markers

            if not_sentence and is_short and is_heading:
                if extra:
                    extra_notes += f'* {curline.strip(". ")}\n'
                    in_extra = True
                else:
                    raw_notes.append([curline, ""])
                    in_extra = False
            else:
                if in_extra:
                    extra_notes += f'        * {curline.strip(". ")}\n'
                    in_extra = False
                else:
                    raw_notes[-1][1] += f"{curline}\n"

        for topic in range(len(raw_notes)):
            notes += f"\n* {raw_notes[topic][0]}\n"

            prompt = f'Summarize the following text: "{raw_notes[topic][1]}"'
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            number_of_tokens = len(tokenizer(prompt)['input_ids'])
            completion = openai.Completion.create(engine="text-davinci-003", max_tokens=4096-number_of_tokens, prompt=prompt)
            for point in completion.choices[0].text.strip("\n. ").split(". "):
                notes += f"        * {point}\n"

        notes += "\n" + extra_notes
        print(notes)

    return render_template("home.html.j2", input=input, output=notes)
