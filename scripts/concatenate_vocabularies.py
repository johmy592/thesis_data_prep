import sys


def concatenate_and_write(v1,v2,save_location):
    '''
    Write the combined content of two lists of terms to file.
    No duplicate terms are written.
    '''
    concatenated_vocabulary = list(set(v1+v2))
    concatenated_vocabulary.sort()
    print('Writing vocabulary of total ',len(concatenated_vocabulary),' terms')
    wf = open(save_location,'w+')
    for w in concatenated_vocabulary:
        wf.write(w)
        wf.write('\n')
    wf.close()

if __name__ == "__main__":
    if(len(sys.argv) != 4):
        print("Usage: ")
        print("python3 concatenate_vocab.py <vocab1_path> <vocab2_path> <write_path>")
        sys.exit()

    vocab_1 = open(sys.argv[1],'r')
    vocab_2 = open(sys.argv[2],'r')
    save_location = sys.argv[3]

    vocab_list_1 = [line.strip('\n') for line in vocab_1]
    vocab_list_2 = [line.strip('\n') for line in vocab_2]

    vocab_1.close()
    vocab_2.close()

    concatenate_and_write(vocab_list_1, vocab_list_2, save_location)
