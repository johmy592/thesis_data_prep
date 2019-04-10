import sys


def count_tokens(filename):
    '''
    Takes a path to a tokenized textfile and counts
    the number of tokens in the textfile. 
    '''
    text = open(filename,'r')
    num_tokens = 0
    for line in text:
        num_tokens += len(line.split()[:-1])

    return num_tokens
    #return sum(len([line.split().strip('\n') for line in text]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage")
        print("python3 count_tokens.py <path-text>")
        sys.exit()

    textfile = sys.argv[1]
    num_tokens = count_tokens(textfile)
    print("corpus contains ", num_tokens, " tokens")
