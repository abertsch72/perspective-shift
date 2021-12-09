def data_extraction():
    import random

    file_sum = "raw_data/shifted.txt"
    file_raw = "raw_data/original.txt"
    random.seed(42)

    with open(file_sum) as f:
        sums = []
        test_sums = []
        count = 0
        test_count = 0
        for line in f:
            line = line.strip()
            if line != "" and line != "-":
                prob = random.random()
                if prob <= 0.9:
                    sums.append(line )
                    count += 1
                else:
                    test_sums.append(line )
                    test_count +=1



    random.seed(42)

    with open(file_raw) as f:
        orig = []
        test_orig = []
        count = 0
        test_count = 0
        for line in f:
            line = line.strip()
            if line != "" and line != "-":
                line = ": ".join(line.split("\t"))
                prob = random.random()
                if prob <= 0.9:
                    orig.append(line)
                    count += 1
                else:
                    test_orig.append(line )
                    test_count +=1



    with open("data_in/train_original.txt", 'w') as f:
        f.writelines(orig)

    with open("data_in/test_original.txt", 'w') as f:
        f.writelines(test_orig)

    train = {}
    train["original"] = orig
    train["shifted"] = sums
    print(train)
    test = {}
    test["original"] = test_orig
    test["shifted"] = test_sums
    data = {}
    data['train'] = train
    data['test'] = test
    return train, test

