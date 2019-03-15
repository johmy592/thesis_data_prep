# Data preparation

The scripts/ directory contains python scripts for data preparation. 

## Starting point:
    - .txt files that will make up the corpus
    - .xlsx file with terms
    - The SemEval-2018 task 9 data

## End result:
    - corpus, vocabulary and training data on the same format as the SemEval data.

## Requirements:
    - python 3 (tested on 3.5.2)
    - nltk (for WordNet resources)
    - spaCy
    - openpyxl
    - A lot of disk space. About 40 GB to store the UMBC corpus along with the concatenated corpus. Note that even more will be needed later during pre-processing in preparation for model training.
    - The usage guide assumes that `Bash` is used

## Usage
Start by downloading the SemEval-2018 task 9 data (https://competitions.codalab.org/competitions/17119). Both training data and the tokenized UMBC corpus can be found at that link.

Next, we prepare a vocabulary using the terms from the .xlsx file

```bash
python3 make_term_vocab.py [path-xlsx] [save-filepath]
```

Next, we prepare some gold standard training data. [terms-vocab-path] referres to the vocabulary created in the previous step. [full-vocab-path] referres to the full vocabulary that will be used during training. If the final training data is supposed to be purely domain specific data, then the two vocabularies are the same. If it is to be a mix with the SemEval data, the full-vocab referres to the 1A.english.vocabulary.txt file from the SemEval data. 

```bash
python3 create_training_data.py [terms-vocab-path] [full-vocab-path] [save-dir]
```

Next, we compile a tokenized corpus from the .txt files. This step will take a while, depending on the amount of text. [dir-txt] is the directory where the .txt files are located.
 
```bash
python3 make_term_corpus.py [dir-txt] [save-filepath]
```

Now we have domain specific data on a format where it can be pre-processed and used directly by models designed to work on SemEval-2018 Task 9 data. If we want to mix the domain specific data with the SemEval-2018 data, we can do the following:

Concatenate the training data:
```bash
python3 concatenate_training_data.py [SemEval-dir] [domspec-dir] [save-dir]
```
[domspec-dir] is assumed to contain a gold.txt file and a queries.txt file.

Concatenate the vocabularies:
```bash
python3 concatenate_vocab.py [vocab1-path] [vocab2-path] [save-path]
```

Concatenate the corpora:
```bash
python3 concatenate_corpus.py [corpus-path1] [corpus-path2] [save-path]
```

