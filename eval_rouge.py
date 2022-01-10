from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])


def read(filename):
    with open(filename) as f:
        lines = ""
        for line in f:
            line = line.strip()
            if line != "" and line != "-":
                lines += line + " "

    return lines

orig = "raw_data/orig-rouge.txt"
matt = "raw_data/graham.txt"

orig = read(orig)
matt = read(matt)
print(scorer.score(orig, matt))