import random
import sys

NUM_QUERIES = 100

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print("Usage:")
        print("python3 make_queries.py <path-vocab> <save-path>")
        sys.exit()

    vocab_path = sys.argv[1]
    save_path = sys.argv[2]

    vf = open(vocab_path,'r')
    terms_list = [w.strip('\n') for w in vf]
    queries = random.sample(terms_list, NUM_QUERIES)

    sf = open(save_path,'w+')
    for q in queries:
        sf.write(q)
        sf.write('\t')
        sf.write('Concept')
        sf.write('\n')
    sf.close()
