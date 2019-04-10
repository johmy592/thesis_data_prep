import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:")
        print("python3 calc_num_pairs.py path_hypernyms")
        sys.exit()

    path_hypernyms = sys.argv[1]

    hf = open(path_hypernyms, 'r')
    hypernyms_list = [line.split('\t') for line in hf]

    print("Num pairs: ", sum([len(hs) for hs in hypernyms_list]))
