import re
import sys
import spacy
from spacy.tokenizer import Tokenizer
from os import listdir
from os.path import isfile, join


nlp = spacy.load('en', disable=['parser','ner'])

nlp.add_pipe(nlp.create_pipe('sentencizer'))

prefix_re = spacy.util.compile_prefix_regex(nlp.Defaults.prefixes)
suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)
infix_re = spacy.util.compile_suffix_regex(nlp.Defaults.infixes)
#keep_re = re.compile(r'[^ ]*-[^ \n\.\,\t]*')
keep_re = re.compile(r'\w+[\'\’]s')

nlp.tokenizer = Tokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
                                                  prefix_re.search,
                                                  suffix_re.search,
                                                  infix_re.finditer,
                                                  token_match=keep_re.match)
IGNORE_TOKENS = ['༔','༅','༒','༖','༗','']
DIVIDERS = ['༎']
IGNORE_WHOLE_LINE = ['\\']


def get_filenames(files_dir):
    return [f for f in listdir(files_dir) if isfile(join(files_dir, f))]


def replace_div_chars(filename):
    tf = open(filename,'r')
    texts_list = []
    for line in tf:
        ignore_line=False
        for ic in IGNORE_WHOLE_LINE:
            if ic in line:
                ignore_line=True
        if ignore_line:
            continue
        for div in DIVIDERS:
            line = line.replace(div,'\n')
        clean_line = line.split('\n')
        texts_list += [l for l in clean_line if l]
    return texts_list


def extract_text(texts):
    '''
    Currently lowercasing all lines
    '''
    texts_list = []
    for line in texts:
        ignore_line=False
        for ic in IGNORE_WHOLE_LINE:
            if ic in line:
                ignore_line=True
        if ignore_line:
            continue
        clean_line = ""
        for c in line:
            if c in IGNORE_TOKENS:
                if clean_line.strip('\n').strip(' '):
                    texts_list.append(clean_line.replace(u'\xa0', u' ').strip('\n'))
                    clean_line=""
                continue
            clean_line += c
        if clean_line.strip('\n').strip(' '):
            texts_list.append(clean_line.replace(u'\xa0', u' ').strip('\n'))
    return texts_list


def make_tokenized_doc_list(texts_list):
    return [nlp(line) for line in texts_list]


def write_tokenized_text_to_file(doc_list, file_path):
    fp = open(file_path,'w+')
    for doc in doc_list:
        sentences = doc.sents
        for s in sentences:
            line = ""
            for t in s:
                if t.text in [' ','\t']:
                    continue
                #line += t.text
                if t.tag_ in ['NN','NNP','NNPS','NNS'] and (not '\'' in t.text) and (not '’' in t.text):
                    line += t.lemma_
                else:
                    line += t.text
                if t.text != '\n':
                    line += ' '
            if line.strip(' ').strip('\n'):
                fp.write(line)
                fp.write('\n')
    fp.close()


def aggregate_all(files, location):
    intermediate = []
    all_lines = []
    print('Extracting lines from ',len(files), 'files\n')

    for filename in files:
        intermediate += replace_div_chars(texts_dir+filename)

    all_lines = extract_text(intermediate)
    print('Tokenizing ', len(all_lines),'lines.')
    print('This might take several minutes\n')
    docs = make_tokenized_doc_list(all_lines)
    print('Writing to file\n')
    write_tokenized_text_to_file(docs, location)


if __name__ == "__main__":

    if(len(sys.argv) != 3):
        print("Usage: ")
        print("python3 make_term_corpus.py <textst_dir> <save_path>")
        sys.exit()

    texts_dir = sys.argv[1]
    save_location = sys.argv[2]

    files_list = get_filenames(texts_dir)
    aggregate_all(files_list, save_location)
