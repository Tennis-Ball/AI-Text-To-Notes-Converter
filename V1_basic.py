# first basic pass with pure python
# may use nltk.tag WordNet in later versions to more effectively
# identify important, noteworthy sentences
# may develop summarizing algorithm
# https://stackoverflow.com/questions/17669952/finding-proper-nouns-using-nltk-wordnet

import re


test_notes = ""
extra_notes = ""
extra_markers = ["AP", "TIP", "NOTE", "AP®"]
in_extra = False
punctuation = [".", "!", "?"]

with open("example_passage3.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if len(line) > 1]

    for curline in lines:
        not_sentence = curline[-1] not in punctuation
        is_short = len(curline.split()) < 10
        caps = [word[0].isupper() for word in curline.split()]
        is_heading = caps.count(True)/len(caps) > 0.5
        extra = curline.split()[0] in extra_markers

        if not_sentence and is_short and is_heading:
            if extra:
                extra_notes += f"* {curline}\n"
                in_extra = True
            else:
                test_notes += f"* {curline}\n"
                in_extra = False
        else:
            sentences = [sentence for sentence in re.split(r"([.!?])", curline)[:-1] if len(sentence) > 1]
            # print(sentences)

            if in_extra:
                extra_notes += f"        * {sentences[0]}\n"
                if len(sentences) > 1:
                    extra_notes += f"        * {sentences[-1]}\n"
                in_extra = False
            else:
                test_notes += f"        * {sentences[0]}\n"
                if len(sentences) > 1:
                    test_notes += f"        * {sentences[-1]}\n"
f.close()

print(test_notes)
print()
print(extra_notes)
