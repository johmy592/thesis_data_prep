import sys
import random
import copy

NUM_QUERIES = 300


def make_hypernym_dict(lines_list):
    lines_copy = copy.deepcopy(lines_list)
    hypernym_dict = {}
    lines_with_definitions = [line for line in lines_copy if line[2] not in ['hypernyms','hyponyms'] and len(line)>3]
    for line in lines_with_definitions:
        del line[2]
    hyponym_first = [line for line in lines_list if line[2]=='hypernyms']
    hypernym_first = [line for line in lines_list if line[2]=='hyponyms']

    hyponym_first += [line for line in lines_with_definitions if line[2]=='hypernyms']
    hypernym_first += [line for line in lines_with_definitions if line[2]=='hyponyms']
    for line in hyponym_first:
        hyponym = line[0]
        hypernyms = line[3:]
        if not hyponym.replace('Thesaurus:','').lower() in hypernym_dict:
            hypernym_dict[hyponym.replace('Thesaurus:','').lower()] = hypernyms
        else:
            hypernym_dict[hyponym.replace('Thesaurus:','').lower()] += hypernyms

    for line in hypernym_first:
        hypernym = line[0]
        hyponyms = line[3:]
        for h in hyponyms:
            if not h.replace('Thesaurus:','').lower() in hypernym_dict:
                hypernym_dict[h.replace('Thesaurus:','').lower()] = [hypernym]
            else:
                hypernym_dict[h.replace('Thesaurus:','').lower()] += [hypernym]
    # Remove 'Thesaurus:' from hypernyms that have it
    for hyponym in hypernym_dict:
        new_list = [hypernym.replace('Thesaurus:','').lower() for hypernym in hypernym_dict[hyponym]]
        hypernym_dict[hyponym] = new_list
    return hypernym_dict


def filter_oov_words(hypernym_dict, vocab_list):
    new_dict = {}
    removed_hypo = 0
    intersect = set(vocab_list).intersection(list(hypernym_dict.keys()))

    for w in hypernym_dict:
        if w not in intersect:
            removed_hypo += 1
            continue
        else:
            keep_list = [h for h in hypernym_dict[w] if h in vocab_list]
            if keep_list:
                new_dict[w] = keep_list
            else:
                removed_hypo += 1
    print("Removed ", removed_hypo, " oov hyponyms")
    return new_dict

def calculate_avg_num_hypernyms(hypernym_dict):
    print("dict contains ",len(list(hypernym_dict.keys())), "example hyponyms")
    avg_num = sum([len(hypernym_dict[w]) for w in hypernym_dict])/len(list(hypernym_dict.keys()))
    print("with an average of ", avg_num, "hypernyms")


def sample_terms(hypernym_dict, num_samples=100):
    '''
    Returns a random sample of num_samples terms
    '''
    all_terms = [t for t in hypernym_dict]
    sample_size = min(num_samples,len(all_terms))
    if(sample_size != num_samples):
        print("WARNING: Only found ",sample_size, "terms with hypernyms")
    return random.sample(all_terms, sample_size)

def write_training_data(queries, hypernym_dict, query_file, gold_file):
    '''
    Writes a query file and a gold file in accordance with the
    SemEval-2018 Task 9 standard
    '''
    qf = open(query_file,'w+')
    gf = open(gold_file,'w+')
    for q in queries:
        qf.write(q)
        qf.write('\t')
        qf.write('Concept')
        qf.write('\n')
        unique_hypernyms = list(set(hypernym_dict[q]))
        for i in range(len(unique_hypernyms)):
            gf.write(unique_hypernyms[i])
            if not i == (len(unique_hypernyms)-1):
                gf.write('\t')
        gf.write('\n')
    qf.close()
    gf.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:")
        print("python3 wiktionary_training_data.py <wiktionary_path> <vocab_path> <save_dir>")
        sys.exit()

    wiktionary_file = sys.argv[1]
    vocab_file = sys.argv[2]
    save_dir = sys.argv[3]

    wiki_file = open(wiktionary_file, encoding ='utf16', errors='ignore')
    wiki_file.readline() # To skip first line
    all_lines = [[w for w in line.split('\t') if w not in ['\n','']] for line in wiki_file]
    print("Read ", len(all_lines), "lines from wiktionary file")

    hypernym_dict = make_hypernym_dict(all_lines)

    vf = open(vocab_file,'r')
    v_list = [line.strip('\n') for line in vf]
    vf.close()

    print("Removing oov words based on vocab of size ",len(v_list))
    ready_hypernyms = filter_oov_words(hypernym_dict, v_list)

    print("Stats before filtering:")
    calculate_avg_num_hypernyms(hypernym_dict)
    print("Stats after filtering:")
    calculate_avg_num_hypernyms(ready_hypernyms)

    print("Sampling ", NUM_QUERIES, "queries for training data")
    queries = sample_terms(ready_hypernyms,300)

    print("Writing to file")
    write_training_data(queries, ready_hypernyms, save_dir+'queries.txt', save_dir+'gold.txt')
