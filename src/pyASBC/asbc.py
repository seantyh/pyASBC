import re
from pathlib import Path
from enum import Enum, auto
from itertools import chain
from lxml import etree
from tqdm.autonotebook import tqdm
from .asbc_type import Article

class IterateUnit(Enum):
    Character = auto()
    Word = auto()
    Article = auto()

class Asbc5Corpus:
    def __init__(self, corpus_basedir=None):
        if not corpus_basedir:
            corpus_basedir = (Path(__file__).parent / "../../data").resolve().absolute()

        if isinstance(corpus_basedir, str):
            corpus_basedir = Path(corpus_basedir)
        self.corpus_basedir = corpus_basedir
        self.cjk_pat = re.compile(r"[\u3400-\u9FFF\uF900-\uFAFF]+")

    def map_article(self, file_path):
        # print(file_path)
        xmldat_f = file_path.open('r', encoding = 'UTF-8')
        tree = etree.parse(xmldat_f)
        root = tree.getroot()
        for art_elem in root.xpath("/corpus/article"):
            try:
                yield Article(art_elem)
            except Exception as ex:
                print(file_path)
                print(ex)
                
        xmldat_f.close()

    def iter_characters(self, no_punc=True):
        iter_word = self.iter_words_with_pos(no_punc=no_punc)                    
        iter_word = map(lambda x: x[0], iter_word)
        iter_char = chain.from_iterable(iter_word)
        return iter_char

    def iter_words(self, no_punc=True):
        iter_word = map(lambda x: x[0], self.iter_words_with_pos(no_punc))
        return iter_word

    def iter_words_with_pos(self, no_punc=True):
        iter_sent = self.iter_sentences()
        iter_word = chain.from_iterable(iter_sent)
        if no_punc:
            iter_word = filter(lambda x: not x[1].endswith("CATEGORY"), iter_word)
            iter_word = filter(lambda x: not x[1].endswith("FW"), iter_word)
        return iter_word

    def iter_sentences(self):
        iter_art = self.iter_articles()
        iter_sent = map(lambda x: x.text.sentences, iter_art)
        iter_sent = chain.from_iterable(iter_sent)
        return iter_sent

    def iter_articles(self):
        iter_file = self.iter_files()
        iter_art = map(self.map_article, iter_file)
        iter_art = chain.from_iterable(iter_art)
        return iter_art

    def iter_files(self):
        basedir = self.corpus_basedir
        xmlfiles = chain((basedir/"ASBC_A").iterdir(),
                        (basedir/"ASBC_B").iterdir())
        xmlfiles = filter(lambda x: x.suffix == ".xml", xmlfiles)
        return xmlfiles


