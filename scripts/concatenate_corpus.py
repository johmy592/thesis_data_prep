import sys


def concatenate_files(filename1, filename2, write_filename):
    '''
    Concatenates two textfiles and write the full content
    to a new file. Writen to work for big files.
    '''
    f1 = open(filename1,'r')
    f2 = open(filename2,'r')
    wf = open(write_filename,'w+')
    line_num = 0
    for line in f1:
        line_num += 1
        wf.write(line)
        if((line_num % 10000000) == 0):
            print("Wrote ",str(line_num),"lines\n")
    f1.close()
    print("First file done!\n")
    line_num = 0
    for line in f2:
        line_num += 1
        wf.write(line)
        if((line_num % 10000000) == 0):
            print("Wrote ",str(line_num),"lines\n")
        wf.write(line)
    print("Wrote ", str(line_num), "lines from second file\n")
    f2.close()
    wf.close()


if __name__ == "__main__":

    if(len(sys.argv) != 4):
        print("Usage:")
        print("python3 concatenate_corpus.py <corpus_path1> <corpus_path2> <save_path>")
        sys.exit()

    first_corpus = sys.argv[1]
    second_corpus = sys.argv[2]
    save_file = sys.argv[3]

    concatenate_files(first_corpus, second_corpus, save_file)
