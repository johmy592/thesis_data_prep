import sys
import re
from os import listdir
from os.path import isfile, join
import spacy
from spacy.tokenizer import Tokenizer

IGNORE_TOKENS = ['༔','༅','༒','༖','༗','']
DIVIDERS = ['༎']
IGNORE_WHOLE_LINE = ['\\']

IGNORE_WORDS = ['the','The', 'a', 'an', 'and','A','And']
STRIP_CHARS = ['"','&','(',')','®','►']

nlp = spacy.load('en_core_web_sm')

prefix_re = spacy.util.compile_prefix_regex(nlp.Defaults.prefixes)
suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)
infix_re = spacy.util.compile_suffix_regex(nlp.Defaults.infixes)
#keep_re = re.compile(r'[^ ]*-[^ \n\.\,\t]*')
keep_re = re.compile(r'\w+[\'\’]s')

new_tokenizer = Tokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
                                                  prefix_re.search,
                                                  suffix_re.search,
                                                  infix_re.finditer,
                                                  token_match=keep_re.match)

nlp.tokenizer = new_tokenizer

"""
TODO: Make a separate file for utility
functions and move out some stuff
"""
def get_filenames(files_dir):
    return [f for f in listdir(files_dir) if isfile(join(files_dir, f))]

def strip_tibet_chars(filename):
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

def get_noun_chunks(doc_list):
    return [d.noun_chunks for d in doc_list if d.noun_chunks]

def get_pruned_nc_texts(nc_list):
    nc_texts = []
    for ncs in nc_list:
        for nc in ncs:
            ts = nc.text.split()
            text = ""
            for t in ts:
                for sc in STRIP_CHARS:
                    t = t.replace(sc,'')
                if not t:
                    continue
                if t not in IGNORE_WORDS:
                    text += t
                    text += " "
            if len(text[:-1].split()) < 4 and text.replace(' ',''):
                nc_texts.append(text[:-1].lower())
    return nc_texts

def lemmatize_texts(lemmatizer, texts_list):
    return [lemmatizer.lemmatize(t) for t in texts_list]

def write_to_file(texts,save_location):
    wf = open(save_location,'w+')
    for t in texts:
        wf.write(t)
        wf.write('\n')
    wf.close()

def concatenate_with_vocab(chunks_file, vocab_file):
    cf = open(chunks_file,'r')
    vf = open(vocab_file, 'r')
    cws = [line.strip('\n') for line in cf]
    vws = [line.strip('\n') for line in vf]
    tot = list(set(cws+vws))
    tot.sort()
    cf.close()
    vf.close()
    return tot

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python3 get_noun_chunks <tokenized_text_path> <save_location>")
        sys.exit()

    tokenized_text_location = sys.argv[1]
    save_location = sys.argv[2]

    tts = open(tokenized_text_location,'r')
    texts_from_corpus = [line.strip('\n') for line in tts]
    tts.close()

    print("Processing ",len(texts_from_corpus), " lines in nlp pipeline")
    print("This might take several minutes")
    docs = make_tokenized_doc_list(texts_from_corpus)

    print("Extracting noun chunks")
    noun_chunks = get_noun_chunks(docs)
    chunk_texts = get_pruned_nc_texts(noun_chunks)
    unique_chunks = list(set(chunk_texts))
    unique_chunks.sort()
    print("Found ", len(unique_chunks), " unique noun chunks")

    print("Writing to file")
    write_to_file(unique_chunks, save_location)
    
