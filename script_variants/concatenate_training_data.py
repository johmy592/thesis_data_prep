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


if __name__ == "__main__":
    if(len(sys.argv) != 4):
        print("Usage: ")
        print("python3 concatenate_training_data.py <SemEval_dir> <domspec_dir> <save_dir>")
        sys.exit()

    semeval_dir = sys.argv[1]
    domspec_dir = sys.argv[2]
    save_dir = sys.argv[3]

    qf1 = semeval_dir + "training/data/1A.english.training.data.txt"
    qf2 = domspec_dir + "queries.txt"
    
    gf1 = semeval_dir + "training/gold/1A.english.training.gold.txt"
    gf2 = domspec_dir + "gold.txt"

    write_queries = save_dir + "concat_queries.txt"
    write_gold = save_dir + "concat_gold.txt"
    
    concat_training_data(qf1,qf2,gf1,gf2,write_queries,write_gold)
