import pandas as pd
from AutoClean import AutoClean

def auto_clean(df: pd.DataFrame):
    cleaner = AutoClean(df, mode = 'manual', duplicates='auto', missing_num='auto', missing_categ='delete', 
          encode_categ=['label'], extract_datetime=False, outliers='delete', outlier_param=1.5, 
          logfile=True, verbose=False)
    return cleaner.output

def category_convert(df: pd.DataFrame, columns: tuple):
    for column in columns:
        df[column] = df[column].astype('category').cat.codes

def remove_columns(df: pd.DataFrame, columns: tuple):
    for column in columns:
        del df[column]

def float_convert(df: pd.DataFrame, columns: tuple):
    for column in columns:
        df[column] = df[column].astype('float')

def int_convert(df: pd.DataFrame, columns: tuple):
    for column in columns:
        df[column] = df[column].astype('int')
