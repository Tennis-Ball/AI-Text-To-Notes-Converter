# TODO: Settings for textbook and formatting, bullets instead of asterisks

from app import app
from flask import render_template, request, flash, redirect
import openai
from transformers import GPT2Tokenizer
import os

# with open("OPENAI_API_KEY.txt", "r") as k:
#    openai.api_key = k.readline()
#    k.close()
openai.api_key = os.environ["OPENAI_API_KEY"]


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
extra_markers = ["AP", "TIP", "NOTE", "AP®", "Continuity and Change", "Analyzing Evidence", " Causation", " Comparison"]
punctuation = [".", "!", "?"]

@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route("/", methods=["GET", "POST"])
def home():
    notes = ""
    extra_notes = ""
    in_extra = False
    raw_notes = []

    input = ""

    if request.method == "POST":
        input = request.form["text_in"]
        lines = [line.strip() for line in input.split("\n") if len(line) > 1]  # TODO: failure point
       
        for curline in lines:
            not_sentence = curline[-1] not in punctuation
            is_short = len(curline.split()) < 10
            caps = [word[0].isupper() for word in curline.split()]
            is_heading = caps.count(True)/len(caps) > 0.5
            extra = any([marker in curline for marker in extra_markers])

            if not_sentence and is_short and is_heading:
                if extra:
                    extra_notes += f'• {curline.strip(". ")}\n'
                    in_extra = True
                else:
                    raw_notes.append([curline, ""])
                    in_extra = False
            else:
                if in_extra:
                    extra_notes += f'        • {curline.strip(". ")}\n'
                    in_extra = False
                else:
                    if len(raw_notes) == 0:
                        raw_notes.append([curline, ""])
                    else:
                        raw_notes[-1][1] += f"{curline}\n"

        for topic in range(len(raw_notes)):
            notes += f"\n• {raw_notes[topic][0]}\n"

            prompt = f'Summarize the following text: "{raw_notes[topic][1]}"'
            number_of_tokens = len(tokenizer(prompt)['input_ids'])
            print(number_of_tokens)
            if number_of_tokens > 4000:
                flash(f"{raw_notes[topic][1]}", "danger")
                break

            try:
                completion = openai.Completion.create(engine="text-davinci-003", max_tokens=4096-number_of_tokens, prompt=prompt)
            except openai.error.ServiceUnavailableError:
                flash("OpenAI servers are currently overloaded or not ready yet. Please try again shortly.", "danger")
                break

            for point in completion.choices[0].text.strip("\n. ").split(". "):
                notes += f"        • {point}\n"

        notes += "\n\nAP Notes and Tips:\n" + extra_notes
        notes = notes.strip('" ')

    return render_template("home.html.j2", input=input, output=notes)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html.j2")
