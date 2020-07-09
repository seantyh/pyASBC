from import_pyASBC import pyASBC
from collections import Counter
from tqdm import tqdm
import pickle

def main(mode, corpus_path=None):
    print(f"generate {mode} lexicon")
    asbc = pyASBC.Asbc5Corpus(corpus_path)
    if mode == "words":
        counter = Counter(x for x in tqdm(asbc.iter_words()))
    elif mode == "words_pos":
        counter = Counter(x for x in tqdm(asbc.iter_words_with_pos()))
    elif mode == "characters":
        counter = Counter(x for x in tqdm(asbc.iter_characters(no_punc=True)))
    
    print("output to pickle")
    with open(f"asbc5_{mode}.pkl", "wb") as fout:
        pickle.dump(counter, fout)

    fout = open(f"asbc5_{mode}.csv", "w", encoding="UTF-8")
    for key, value in tqdm(counter.most_common(), desc="writing csv"):
        if mode == "words_pos":
            fout.write(f"{key[0]}, {key[1]}, {value}\n")
        else:
            fout.write(f"{key}, {value}\n")
    fout.close()    

if __name__ == "__main__":
    # main("characters", "../ASBC_test")
    # main("words", "../ASBC_test")
    # main("words_pos", "../ASBC_test")
    print ("=== Characters ===")
    main("characters")
    # print ("=== Words ===")
    # main("words")
    # print ("=== Words(POS) ===")
    # main("words_pos")