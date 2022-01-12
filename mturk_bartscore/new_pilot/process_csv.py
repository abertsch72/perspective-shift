import csv
import os

def get_csv_info():
    id = 15
    indices = [80, 86, 87, 88, 89, 90, 91, 92, 93, 81, 82, 83, 84, 85]
    with open('Batch_4643619_batch_results.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader) # skip the header line

        for row in reader:
            output = ""
            for i in indices:
                output += row[i] + "\n"
            print(output)
            with open("annotator_out/" + row[id] + ".txt", 'w') as f:
                f.write(output)



def unclean(turn):

    turn = turn.replace("&amp", "&")
    turn = turn.replace("&lt", "<")
    turn = turn.replace("&gt", ">")
    turn = turn.replace("&quot", '"')
    turn = turn.replace("&#39", "'")
    turn = turn.replace("&#44", ",")

    return turn


def get_csv_annotations(filename):
    split_message = "This rephrasing was challenging</crowd-checkbox></td></tr><tr class=\"d-flex\"><th scope=\"row\" ></th>"
    # todo: need to write table parsing code here!!

    # todo: find indices of annotation values
    indices = [32, 39, 40, 41, 42, 43, 44, 45, 46, 33, 34, 35, 36, 37, 38]
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader) # skip the header line

        output = ""
        inputs = ""
        for row in reader:
            lines = row[30].split("tbody>")[1].split(split_message)
            for line in lines:
                utterance = line.split("<td>")
                utterance = utterance[1].split("</td>")[0] + "\t" + unclean(utterance[3].split("</td>")[0])
                inputs += utterance + "\n"
            for i in indices:
                # todo: check if this is what an empty row looks like
                if row[i] != "":
                    output += row[i] + "\n"
            output += "\n"
            inputs += "\n"
            print(output)

    with open("annotations.txt", 'w') as f:
        f.write(output)

    with open("annotated.txt", 'w') as f:
        f.write(inputs)


#get_csv_annotations("../../raw_data/Batch_4644771_batch_results.csv")
get_csv_annotations("../../raw_data/Batch_4644768_batch_results.csv")