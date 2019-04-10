import sys

def concat_training_data(qf1, qf2, gf1, gf2, write_q, write_g):
    _wq = open(write_q,'w+')
    _qf1 = open(qf1,'r')
    for line in _qf1:
        _wq.write(line)
    _qf1.close()
    _wq.write('\n')
    _qf2 = open(qf2,'r')
    for line in _qf2:
        _wq.write(line)
    _qf2.close()
    _wq.close()

    _wg = open(write_g,'w+')
    _gf1 = open(gf1,'r')
    for line in _gf1:
        _wg.write(line)
    _gf1.close()
    _gf2 = open(gf2,'r')
    _wg.write('\n')
    for line in _gf2:
        _wg.write(line)
    _gf2.close()
    _wg.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:")
        print("python3 aggregate_domspec_training_data.py <wordnet-dir> <wiktionary-dir> <save-dir>")
        sys.exit()

    wn_folder = sys.argv[1]
    wiki_folder = sys.argv[2]
    save_dir = sys.argv[3]

    qf1 = wn_folder+'queries.txt'
    qf2 = wiki_folder+'queries.txt'

    gf1 = wn_folder+'gold.txt'
    gf2 = wiki_folder+'gold.txt'

    write_q = save_dir+'queries.txt'
    write_g = save_dir+'gold.txt'

    #concat_training_data(qf1, qf2, gf1, gf2, write_q, write_g)

    wn_queries = [line.split('\t')[0] for line in open(qf1,'r')]
    wiki_queries = [line.split('\t')[0] for line in open(qf2,'r')]

    wiki_only = [q for q in wiki_queries if q not in wn_queries]
    print(wiki_only)
