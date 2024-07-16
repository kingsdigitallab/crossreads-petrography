import os
import pandas as pd
import numpy as np


def try_float(x):
    try:
        return float(x)
    except (ValueError,TypeError):
        return np.nan
    
def clean_sample_num(x):
    if not x:
        return x
    x = x.strip().split()[0].split('-')[0]
    return ''.join(y for y in x if y.isdigit())

def extract_sample_id(filename):
    noext=os.path.splitext(filename)[0]
    before, suffix=os.path.split(noext)
    if 'ISic' in before:
        return f'ISic{suffix}'
    return suffix

def clean_params(x):
    if x in {'Qcalcitemg', 'Qcalcitmg'}:
        return 'QMgCalcite'
    return x

def sum_columns(row, columns):
    return sum(float(row.get(col, 0)) for col in columns if pd.notna(row.get(col)))

def is2(x):
    if x is np.nan: return False
    if not x: return False
    return True

def value_was_updated(x,y):
    x=str(x)
    y=str(y)
    if y=='nan': return False
    return x != y