from nltk.corpus import wordnet as wn
import random
import sys

# Arguments from command line:
#       - domain specific vocabulary
#       - full vocabulary (to be considered when filtering oov hypernyms
#       - save directory

# Add terms to this list if they should be ignored as gold hypernyms
OVERLY_GENERAL = ['artifact']

LEVELS = 5
NUM_QUERIES = 300


def check_synsets(terms):
    '''
    Returns a list with all terms that have a wordnet synset
    '''
    return [w for w in terms if wn.synsets(w.replace(' ','_'))]


def select_single_synset(terms_with_synsets):
    '''
    Returns a dictionary with first available synset with a
    noun POS tag
    '''
    synset_dict = {}
    for t in terms_with_synsets:
        ss = wn.synsets(t.replace(' ','_'))
        for s in ss:
            if '.n' in s.name():
                synset_dict[t] = s
                break
    return synset_dict    


def select_all_synsets(terms_with_synsets):
    '''
    Returns a list with all synsets with a noun
    POS tag
    '''
    synset_dict = {}
    for t in terms_with_synsets:
        ss = wn.synsets(t.replace(' ','_'))
        for s in ss:
            if '.n' in s.name():
                if t in synset_dict:
                    synset_dict[t].append(s)
                else:
                    synset_dict[t] = [s]
    return synset_dict


def make_hypernym_dict2(synset_dict, num_levels=2):
    '''
    Returns a dictionary of terms associated with
    its hypernym synsets, traverses num_levels levels
    in the wordnet hierarchy. 
    Assumes each term is associated with a list of Synsets,
    as opposed to a single one.
    '''
    hypernym_dict = {}
    for term in synset_dict:
        for ss in synset_dict[term]:
            cur_level = 0
            next_hypernyms = ss.hypernyms()
            if term in hypernym_dict:
                hypernym_dict[term] += next_hypernyms
            else:
                hypernym_dict[term] = next_hypernyms
            cur_level += 1
            while cur_level < num_levels:
                _next_hypernyms = []
                for h in next_hypernyms:
                    _next_hypernyms += h.hypernyms()
                hypernym_dict[term] += _next_hypernyms
                next_hypernyms = _next_hypernyms
                cur_level += 1
    return hypernym_dict


def make_hypernym_dict(synset_dict,num_levels=2):
    '''
    Returns a dictionary of terms associated with
    its hypernym synsets, traverses num_levels levels
    in the wordnet hierarchy
    '''
    hypernym_dict = {}
    for term in synset_dict:
        cur_level = 0
        next_hypernyms = synset_dict[term].hypernyms()
        
        hypernym_dict[term] = next_hypernyms
        cur_level += 1
        while cur_level < num_levels:
            _next_hypernyms = []
            for h in next_hypernyms:
                _next_hypernyms += h.hypernyms()
            hypernym_dict[term] += _next_hypernyms
            next_hypernyms = _next_hypernyms
            cur_level += 1
            
    return hypernym_dict


def keep_vocab_hypernyms(hypernym_dict, full_vocab_list):
    '''
    Removes hypernyms that do not exist in the
    vocabulary
    '''
    processed_terms = 0
    new_dict = {}
    for term in hypernym_dict:
        hypernyms_to_keep = []
        for h in hypernym_dict[term]:
            hypernym_text = h.name().split('.n')[0].replace('_',' ') 
            if (hypernym_text in full_vocab_list) and not ( hypernym_text in OVERLY_GENERAL):
                hypernyms_to_keep += [hypernym_text]
        if hypernyms_to_keep:
            new_dict[term] = hypernyms_to_keep
        processed_terms += 1
        if processed_terms%100 == 0:
            print("Processed ", str(processed_terms), " terms")
    print("Done processing terms!")
    return new_dict


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


def sanity_check(hypernym_dict, full_vocab_list):
    '''
    Performs a sanity check to make sure that no 
    out-of-vocabulary terms remain
    '''
    for term in hypernym_dict:
        if term not in full_vocab_list:
            print("Found out of vocab term: ", term ," something went wrong!")
            return
        for h in hypernym_dict[term]:
            if h not in full_vocab_list:
                print("Found out of vocab term: ", h , " something went wrong!")
                return
    print("All good!\n")


def print_help():
    print("Usage: ")
    print("python3 create_training_data.py <terms_vocab_path> <full_vocab_path> <save_dir>")

if __name__ == "__main__":
   
    if(not len(sys.argv) == 4):
        print_help()
        sys.exit() 
    terms_vocab = sys.argv[1]
    full_vocab = sys.argv[2]
    save_folder = sys.argv[3]
    query_file = save_folder + 'queries.txt'
    gold_file = save_folder + 'gold.txt'

    tf = open(terms_vocab,'r')
    terms_list = [w.strip('\n') for w in tf]
    tf.close()
    print("Read ", len(terms_list), " terms from vocabulary")
    
    terms_with_synsets = check_synsets(terms_list)
    print("Found ", len(terms_with_synsets), " terms with wordnet synsets")

    term_synset_dict = select_all_synsets(terms_with_synsets)
    hypernym_dict = make_hypernym_dict2(term_synset_dict,num_levels=LEVELS)
    print("Added hypernyms across ",LEVELS, " levels")

    fvf = open(full_vocab,'r')
    full_vocab_list = [w.strip('\n') for w in fvf]
    fvf.close()
    print("Removing oov words based on vocab of size ", len(full_vocab_list))

    ready_hypernyms = keep_vocab_hypernyms(hypernym_dict, full_vocab_list)
    
    print("Selecting random sample of ", NUM_QUERIES, " queries")
    queries = sample_terms(ready_hypernyms, NUM_QUERIES)

    print("Writing to file")
    write_training_data(queries, ready_hypernyms, query_file, gold_file)
