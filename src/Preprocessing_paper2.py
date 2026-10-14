import re, sys, os
from typing import Iterable, Optional
 
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
# print(ROOT_DIR)
sys.path.insert(0, str(ROOT_DIR))

from config.config_script import KEEP_WORDS, DEFAULT_NORM_DICT
 
class TextPreprocessing_Paper2:
    """
    Parameters
    ----------
    keep_negation : bool
        False -> stopword murni dari daftar sumber (meniru paper secara literal).
        True  -> daftar stopword dikurangi KEEP_WORDS.
    stopword_source : {'nltk', 'sastrawi'} atau iterable kata
        Sumber daftar stopword (asumsi, paper tidak menyebut).
    keep_words : iterable[str], optional
        Mengganti KEEP_WORDS bawaan (hanya berlaku jika keep_negation=True).
    norm_dict : dict, optional
        Kamus normalisasi. Default: DEFAULT_NORM_DICT.
    normalize_first : bool
        True  -> cleaning -> normalization -> stopword (urutan yang disarankan).
        False -> cleaning -> stopword -> normalization (urutan literal di paper).
    output : {'string', 'tokens'}
        'string' untuk TF-IDF/IndoBERT, 'tokens' untuk Bi-LSTM.
    """
 
    def __init__(
        self,
        keep_negation: bool = False,
        stopword_source='nltk',
        keep_words: Optional[Iterable[str]] = None,
        norm_dict: Optional[dict] = None,
        normalize_first: bool = True,
        output: str = 'string',
    ):
        if output not in ('string', 'tokens'):
            raise ValueError("output has to be 'string' or 'tokens'")
        
        self.keep_negation = keep_negation
        self.stopword_source = stopword_source
        self.keep_words = set(keep_words) if keep_words is not None else set(KEEP_WORDS)
        self.norm_dict = dict(norm_dict) if norm_dict is not None else dict(DEFAULT_NORM_DICT)
        self.normalize_first = normalize_first
        self.output = output
        self.stopwords_ = self._build_stopwords()
 
    # ---------- stopwords ----------
    def _load_base_stopwords(self) -> set:
        src = self.stopword_source
        if isinstance(src, str):
            if src == 'nltk':
                import nltk
                try:
                    from nltk.corpus import stopwords
                    return set(stopwords.words('indonesian'))
                except LookupError:
                    nltk.download('stopwords', quiet=True)
                    from nltk.corpus import stopwords
                    return set(stopwords.words('indonesian'))
            if src == 'sastrawi':
                from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
                return set(StopWordRemoverFactory().get_stop_words())
            raise ValueError("stopword_source string harus 'nltk' atau 'sastrawi'")
        return set(src)
 
    def _build_stopwords(self) -> set:
        base = self._load_base_stopwords()
        return base - self.keep_words if self.keep_negation else base
 
    # ---------- tahap preprocessing ----------
    def case_folding(self, text: str) -> str:
        return text.lower()
 
    def data_cleaner(self, text: str) -> str:

        if text.isna() == True:
            text = text.fillna("").astype(str)
            
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)    # URL
        text = re.sub(r'[@#]\w+', ' ', text)                  # username, hashtag
        text = re.sub(r'[^a-z\s]', ' ', text)                 # punctuation, numbers, emoji, unique character
        text = re.sub(r'\s+', ' ', text).strip()              # double spaces or more.
        return text
 
    def normalization(self, text: str) -> str:
        return ' '.join(self.norm_dict.get(t, t) for t in text.split())
 
    def stopword_remover(self, text: str) -> str:
        return ' '.join(t for t in text.split() if t not in self.stopwords_)
 
    def tokenizer(self, text: str) -> list:
        return text.split()
 
    # ---------- pipeline ----------
    def _process_one(self, text):
        text = '' if pd.isna(text) else str(text)
        text = self.case_folding(text)
        text = self.data_cleaner(text)
        if self.normalize_first:
            text = self.normalization(text)
            text = self.stopword_remover(text)
        else:
            text = self.stopword_remover(text)
            text = self.normalization(text)
        if self.output == 'tokens':
            return self.tokenizer(text)
        return text
 
    def fit_transform(self, X) -> pd.Series:
        s = X if isinstance(X, pd.Series) else pd.Series(list(X))
        return s.map(self._process_one)
 
    # ---------- utilitas untuk dokumentasi ----------
    def describe(self) -> dict:
        return {
            'keep_negation': self.keep_negation,
            'stopword_source': self.stopword_source if isinstance(self.stopword_source, str) else 'custom',
            'n_stopwords': len(self.stopwords_),
            'kept_from_stoplist': sorted(self.keep_words & self._load_base_stopwords()) if self.keep_negation else [],
            'normalize_first': self.normalize_first,
            'output': self.output,
        }
 
 
if __name__ == '__main__':
    contoh = pd.Series([
        'GK bisa daftar, bahaya ini!! mohon dicoba kembali',
        'Aplikasinya sangat bagus sekali, tapi kurang responsif :)',
        'tlng jwbany lbih dipejlas',
    ])
    for flag in (False, True):
        p = TextPreprocessing_Paper2(keep_negation=flag)
        print(f'keep_negation={flag}', p.describe())
        print(p.fit_transform(contoh).tolist(), '\n')