# first basic pass with pure python
# may use nltk.tag WordNet in later versions to more effectively
# identify important, noteworthy sentences
# may develop summarizing algorithm
# https://stackoverflow.com/questions/17669952/finding-proper-nouns-using-nltk-wordnet

import re


test_notes = ""
punctuation = [".", "!", "?"]

with open("example_passage.txt", "r", encoding="unicode") as f:
    lines = [line.strip() for line in f if len(line) > 1]

    for curline in lines:
        not_sentence = curline[-1] not in punctuation
        is_short = len(curline.split()) < 10
        caps = [word[0].isupper() for word in curline.split()]
        is_heading = caps.count(True)/len(caps) > 0.5

        if not_sentence and is_short and is_heading:
            test_notes += f"* {curline}\n"
        else:
            sentences = [sentence for sentence in re.split(r"([.!?])", curline)[:-1] if len(sentence) > 1]
            print(sentences)

            test_notes += f"    * {sentences[0]}\n"
            if len(sentences) > 1:
                test_notes += f"    * {sentences[-1]}\n"
f.close()

print(test_notes)
