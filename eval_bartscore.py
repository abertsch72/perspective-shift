import os
from BARTScore.bart_score import BARTScorer
bart_scorer = BARTScorer(device='cpu', checkpoint='facebook/bart-large-cnn')


bart_scorer.load(path='BARTScore/bart.pth')


def read_lines(filename):
    with open(filename) as f:
        indices = [0]
        lines = []
        for line in f:
            line = line.strip()
            if line != "" and line != "-":
                lines.append(line)
            else:
                indices.append(len(lines))
        indices.append(len(lines))
        indices = list(sorted(set(indices)))

    return lines, indices

def avg(x):
    return sum(x)/len(x)

def score(outputs, indices):
    #print(str(sum(outputs)/len(outputs)))

    partials = []
    for i in range(len(indices) - 1):
        partials.append(avg(outputs[indices[i]:indices[i+1]]))
    #print("document avg: " + str(avg(partials)))

    return sum(outputs)/len(outputs)


def eval_all(golds, outputs):
    invalid = ['I ', ' we ', ' me ', ' I', ' you', ':)', '!',] # '?', '"']
    comparisons = []
    for file in os.listdir(golds):
        comparisons.append((file.split(".txt")[0], *read_lines(golds + "/" + file)))

    workers = []
    for file in os.listdir(outputs):
        workers.append((file.split(".txt")[0], read_lines(outputs + "/" + file)[0]))

    for comper in comparisons:
        print(comper[0] + "\t", end="")
        for comp in comparisons:
            print(str(score(bart_scorer.score(comp[1], comper[1]), comp[2])) + "\t", end = "")
        detected = False
        for line in comp[1]:
            if len(line.split(" ")) < 2:
                detected = True
                break
            for thing in invalid:
                if thing in line.lower():
                    detected = True
                    break
            if detected:
                break

        print(not detected)

    for worker in workers:
        print(worker[0] + "\t", end = "")
        for comp in comparisons:
            print(str(score(bart_scorer.score(comp[1], worker[1]), comp[2])) + "\t", end = "")
        detected = False

        for line in worker[1]:
            if len(line.split(" ")) < 2:
                detected = True
                break
            for thing in invalid:
                if thing in line.lower():
                    detected = True
                    break
            if detected:
                break

        print(not detected)


"""
orig = "mturk_bartscore/originals/convo5.txt"
mine = "mturk_bartscore/my_anno/convo5.txt"
worker1 = "mturk_bartscore/convo5_A2WL58SGBL598E.txt"
worker2 = "mturk_bartscore/convo5_A17K1867U066SG.txt"
worker3 = "mturk_bartscore/convo4_A3W3TEOEEF4Z3X.txt"

orig, indices = read_lines(orig)
mine, _ = read_lines(mine)
worker1, _ = read_lines(worker1)
worker2, _ = read_lines(worker2)
worker3, _ = read_lines(worker3)

print("me and orig:")
print(score(bart_scorer.score(orig, mine), indices))

print("w1 and orig:")
print(score(bart_scorer.score(orig, worker1), indices))

print("w2 and orig:")
print(score(bart_scorer.score(orig, worker2), indices))

print("w3 and orig:")
print(score(bart_scorer.score(orig, worker3), indices))
"""
eval_all('mturk_bartscore/new_pilot/comparison_files', 'mturk_bartscore/new_pilot/annotator_out')