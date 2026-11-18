from pathlib import Path
import sys, os

ROOT_DIR = Path(__file__).resolve().parents[1]
print(f"ROOT DIR: {ROOT_DIR}")

RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw' / 'WeightedSentimentTelemedicineDataset.csv'
PREPROCESSED_WEIGHTED_DATA_DIR = ROOT_DIR / 'data' / 'preprocessed' / 'Weighted_Sentiment.csv'
WEIGHTED_SPLIT_DATA_DIR = ROOT_DIR / 'data' / 'preprocessed' / 'split' 

# artifact
ARTIFACT_DIR = ROOT_DIR / 'artifact'
VECTORIZER_DIR = ARTIFACT_DIR / 'vectorizer'
MODEL_DIR = ARTIFACT_DIR / 'model'

#Vectorizer
TFIDF_DIR = VECTORIZER_DIR / 'tfidf.joblib'
INDOBERT_DIR = VECTORIZER_DIR / 'indobert.joblib'

#Model
SVM_DIR = MODEL_DIR / 'svm.joblib'

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