from pathlib import Path
import sys, os

ROOT_DIR = Path(__file__).resolve().parent
print(f"ROOT DIR: {ROOT_DIR}")

DATA_DIR = ROOT_DIR / 'data' / 'WeightedSentimentTelemedicineDataset.csv'

# Kata negasi, kontras, dan intensifier yang dipertahankan saat keep_negation=True.
KEEP_WORDS = {
    'tidak', 'tak', 'bukan', 'belum', 'jangan', 'kurang', 'tanpa',
    'tapi', 'tetapi', 'namun', 'padahal',
    'sangat', 'sekali', 'lebih',
    'ga', 'gak', 'nggak', 'gk', 'engga', 'enggak', 'tdk',
}
 
# Kamus normalisasi AWAL (asumsi). Perluas dari kata paling sering di datamu.
DEFAULT_NORM_DICT = {
    'gk': 'tidak', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak',
    'engga': 'tidak', 'enggak': 'tidak', 'tdk': 'tidak', 'tak': 'tidak',
    'blm': 'belum', 'sy': 'saya', 'aja': 'saja', 'bgt': 'banget', 'bgs': 'bagus',

    'tlng': 'tolong', 'tlg': 'tolong',

    'lbih': 'lebih', 'lbh': 'lebih',

    'jwbany': 'jawabannya', 'jwb': 'jawab',

    'yg': 'yang', 'dg': 'dengan', 'dgn': 'dengan', 'sdh': 'sudah', 'udh': 'sudah',
    'krn': 'karena', 'karna': 'karena', 'utk': 'untuk', 'tp': 'tapi',
    'jg': 'juga', 'trs': 'terus', 'dr': 'dari', 'dpt': 'dapat', 'smpe': 'sampai',

    'org': 'orang', 'tdak': 'tidak', 'bs': 'bisa', 'sm': 'sama', 'jd': 'jadi',
    'd': 'di', 'kpn': 'kapan', 'knp': 'kenapa', 'mantul': 'mantap',  
}