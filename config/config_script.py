from pathlib import Path
import sys, os

ROOT_DIR = Path(__file__).resolve().parents[1]
print(f"ROOT DIR: {ROOT_DIR}")

RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw' / 'WeightedSentimentTelemedicineDataset.csv'
PREPROCESSED_WEIGHTED_DATA_DIR = ROOT_DIR / 'data' / 'preprocessed' / 'Weighted_Sentiment.csv'
WEIGHTED_SPLIT_DATA_DIR = ROOT_DIR / 'data' / 'preprocessed' / 'split' 

# Kata negasi, kontras, dan intensifier yang dipertahankan saat keep_negation=True.
KEEP_WORDS = {
    'tidak', 'tak', 'bukan', 'belum', 'jangan', 'kurang', 'tanpa',
    'tapi', 'tetapi', 'namun', 'padahal',
    'sangat', 'sekali', 'lebih', 'bisa',
    'ga', 'gak', 'nggak', 'gk', 'engga', 'enggak', 'tdk',
}
 
# Kamus normalisasi AWAL (asumsi). Perluas dari kata paling sering di datamu.
DEFAULT_NORM_DICT = {
    # negasi
    'gk': 'tidak', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak', 'ngga': 'tidak',
    'engga': 'tidak', 'enggak': 'tidak', 'tdk': 'tidak', 'tak': 'tidak', 'tdak': 'tidak',
    'gabisa': 'tidak bisa', 'gaada': 'tidak ada', 'gaje': 'tidak jelas',
    # umum
    'tlng': 'tolong', 'tlg': 'tolong', 'lbih': 'lebih', 'lbh': 'lebih',
    'jwbany': 'jawabannya', 'jwb': 'jawab', 'yg': 'yang', 'dg': 'dengan', 'dgn': 'dengan',
    'sdh': 'sudah', 'udh': 'sudah', 'udah': 'sudah', 'blm': 'belum', 'sy': 'saya',
    'aja': 'saja', 'bgt': 'banget', 'bgs': 'bagus', 'krn': 'karena', 'karna': 'karena',
    'utk': 'untuk', 'tp': 'tapi', 'jg': 'juga', 'trs': 'terus', 'dr': 'dari', 'dpt': 'dapat',
    'smpe': 'sampai', 'sampe': 'sampai', 'org': 'orang', 'bs': 'bisa', 'sm': 'sama', 'jd': 'jadi',
    'kpn': 'kapan', 'knp': 'kenapa', 'klo': 'kalau', 'klau': 'kalau', 'kalo': 'kalau',
    'thn': 'tahun', 'bnyk': 'banyak', 'gmn': 'bagaimana', 'gimana': 'bagaimana',
    'mantul': 'mantap betul', 'makasih': 'terima kasih', 'trims': 'terima kasih',
    'tks': 'terima kasih', 'thx': 'terima kasih', 'pake': 'pakai', 'pk': 'pakai',
    'hrs': 'harus', 'lg': 'lagi', 'lgi': 'lagi', 'bkn': 'bukan', 'cm': 'cuma', 'cuman': 'cuma',
}