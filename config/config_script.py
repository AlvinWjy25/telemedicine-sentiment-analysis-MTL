from pathlib import Path
import sys, os
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


ROOT_DIR = Path(__file__).resolve().parents[1]
print(f"ROOT DIR: {ROOT_DIR}")

RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw' / 'WeightedSentimentTelemedicineDataset.csv'
PREPROCESSED_WEIGHTED_DATA_DIR = ROOT_DIR / 'data' / 'preprocessed' / 'Weighted_Sentiment.csv'
WEIGHTED_SPLIT_DATA_DIR = ROOT_DIR / 'data' / 'preprocessed' / 'split'

SPLIT_DIR = ROOT_DIR / 'data' / 'splits'
SPLIT_FILE = SPLIT_DIR / 'split_ids.csv'
SPLIT_TEST_SIZE = 0.10
SPLIT_VALIDATION_SIZE = 0.20
SPLIT_RANDOM_STATE = 42

PREPROCESSED_TFIDF_DATA_FILE = PREPROCESSED_WEIGHTED_DATA_DIR.with_name(
    'Weighted_Sentiment_TFIDF.csv'
)
PREPROCESSED_INDOBERT_DATA_FILE = PREPROCESSED_WEIGHTED_DATA_DIR.with_name(
    'Weighted_Sentiment_IndoBERT.csv'
)
TFIDF_SPLIT_DATA_DIR = WEIGHTED_SPLIT_DATA_DIR / 'tfidf'
INDOBERT_SPLIT_DATA_DIR = WEIGHTED_SPLIT_DATA_DIR / 'indobert'

# artifact
ARTIFACT_DIR = ROOT_DIR / 'artifact'
VECTORIZER_DIR = ARTIFACT_DIR / 'vectorizer'

MODEL_DIR = ARTIFACT_DIR / 'model'
MODEL_DIR.mkdir(exist_ok=True, parents=True)

SVM_UNWEIGHTED_DIR = MODEL_DIR / f'SVM_UNWEIGHTED.joblib'
SVM_WEIGHTED_DIR = MODEL_DIR / f'SVM_WEIGHTED.joblib'

#Vectorizer
TFIDF_UNWEIGHTED_DIR = VECTORIZER_DIR / f'TFIDF_UNWEIGHTED.joblib'
TFIDF_WEIGHTED_DIR = VECTORIZER_DIR / f'TFIDF_WEIGHTED.joblib'

# EVAL (DEPRECATED)
# EVAL_DIR = ARTIFACT_DIR / 'evaluation'
# EVAL_DIR.mkdir(exist_ok=True, parents=True)

MODEL_NAME = "indobenchmark/indobert-base-p1"
LABEL2ID = {"NEGATIVE": 0, "NEUTRAL": 1, "POSITIVE": 2}
WEIGHT_MAP_BERT = {
    "UNINFORMATIVE": 0.0,
    "INFORMATIVE": 1.0,
    "COMPLEX": 2.0,
}

INDOBERT_DIR = MODEL_DIR / 'indoBERT_checkpoints'
INDOBERT_DIR.mkdir(parents=True, exist_ok=True)

EVAL_BERT_UNWEIGHTED =  INDOBERT_DIR/ f'results_indobert_unweigthed_{timestamp}'
EVAL_BERT_WEIGHTED = INDOBERT_DIR / f'results_indobert_weighted_{timestamp}'

EVAL_MTL = MODEL_DIR / 'indoBERT_MTL'
EVAL_MTL.mkdir(parents=True, exist_ok=True)

EVAL_BERT_MTL = EVAL_MTL / f'results_MTL_indobert_{timestamp}'
EVAL_CONTROL_BERT_MTL = EVAL_MTL / f'results_control_MTL_indobert_{timestamp}'

#Model
SVM_DIR = MODEL_DIR / f'svm_{timestamp}.joblib'

KEEP_WORDS = {
    'tidak', 'tak', 'bukan', 'belum', 'jangan', 'kurang', 'tanpa',
    'tapi', 'tetapi', 'namun', 'padahal',
    'sangat', 'sekali', 'lebih', 'bisa'
}

# 2. Critical sentiment words that should NEVER be removed
PROTECTED_WORDS = {
    # Negations
    'tidak', 'tak', 'bukan', 'belum', 'jangan', 'kurang', 'tanpa',
    # Contrasts
    'tapi', 'tetapi', 'namun', 'padahal',
    # Degree / Intensifiers
    'sangat', 'sekali', 'lebih', 'paling', 'terlalu'
}

DEFAULT_NORM_DICT = {
    # --- Negation ---
    'gk': 'tidak', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak', 'ngga': 'tidak',
    'engga': 'tidak', 'enggak': 'tidak', 'tdk': 'tidak', 'tak': 'tidak', 'tdak': 'tidak',
    'gabisa': 'tidak bisa', 'gaada': 'tidak ada', 'gaje': 'tidak jelas',
    
    # --- Medical & App terms ---
    'apk': 'aplikasi', 'app': 'aplikasi',
    'rs': 'rumah sakit',
    'konsul': 'konsultasi',
    'fast': 'cepat',
    'aktf': 'aktif',
    
    # --- Prepositions & Conjunctions ---
    'd': 'di',
    'yg': 'yang', 'dg': 'dengan', 'dgn': 'dengan', 'utk': 'untuk', 
    'tp': 'tapi', 'jg': 'juga', 'trs': 'terus', 'dr': 'dari', 'dri': 'dari', 'sm': 'sama', 
    'klo': 'kalau', 'klau': 'kalau', 'kalo': 'kalau', 'krn': 'karena', 'karna': 'karena',
    'jk': 'jika', 'pdhl': 'padahal',
    
    # --- Adverbs, Time & Quantity ---
    'sdh': 'sudah', 'udh': 'sudah', 'udah': 'sudah', 'blm': 'belum', 
    'aja': 'saja', 'bgt': 'banget', 'bgs': 'bagus', 'dpt': 'dapat', 
    'smpe': 'sampai', 'sampe': 'sampai', 'org': 'orang', 'bs': 'bisa', 
    'jd': 'jadi', 'kpn': 'kapan', 'knp': 'kenapa', 'thn': 'tahun', 
    'bnyk': 'banyak', 'gmn': 'bagaimana', 'gimana': 'bagaimana',
    'pake': 'pakai', 'pk': 'pakai', 'hrs': 'harus', 'lg': 'lagi', 
    'lgi': 'lagi', 'bkn': 'bukan', 'cm': 'cuma', 'cuman': 'cuma',
    'dlu': 'dulu', 'tdi': 'tadi', 'ky': 'kayak',
    
    # --- Communication & Particles ---
    'sy': 'saya', 'tlng': 'tolong', 'tlg': 'tolong', 
    'lbih': 'lebih', 'lbh': 'lebih', 'jwbany': 'jawabannya', 'jwb': 'jawab',
    'krja': 'kerja', 'yaudh': 'ya sudah', 'si': 'sih', 'ko': 'kok',
    
    # --- Gratitude & Satisfaction ---
    'makasih': 'terima kasih', 'trims': 'terima kasih', 'tks': 'terima kasih', 
    'thx': 'terima kasih', 'ty': 'terima kasih', 'trimakasih': 'terima kasih', 
    'terimakasih': 'terima kasih', 'mantul': 'mantap betul', 'goodjob': 'good job',
    
    # --- Double letters / Colloquial variants ---
    'baiik': 'baik',
    'siip': 'sip', 'sipp': 'sip',
    'ok': 'oke', 'okee': 'oke', 'okey': 'oke', 'okeyy': 'oke', 'okeh': 'oke',
    'sanga': 'sangat'
}



'''
POSITIVE_KEYWORDS = [
    "oke", "ok", "okee", "okey", "good job", "goodjob", 
    "baik", 'baikk', 'baiik', "bagus", "sip", 'baik dokternya', 'ty',
    "siap", "mantap", 'good', 'terima kasih', 'nice', 'thank you', 'terimakasih',
    'trimakasih', 'sehat selalu', 'sangat berguna', 'okk', 'bagus', 'approved',
    'like', 'wow', 'terimaksih', 'makasih', 'sabar dokternya'
]
'''