import pandas as pd
import numpy as np


def process_file(uploaded_file, interval):
    # Get the file name and determine the file extension
    file_name = uploaded_file.name
    if file_name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, sep=';', decimal=',', skiprows=2)
    elif file_name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, skiprows=2)
    else:
        raise ValueError('File type not supported. Please upload a CSV or Excel file.')
    
    # Processing logic (adapted from your provided code)
    df['DateTime'] = pd.to_datetime(df['Datum'] + ' ' + df['Uhrzeit'], dayfirst=True)
    df.set_index('DateTime', inplace=True)
    df.drop(columns=['Datum', 'Uhrzeit'], inplace=True)

    numeric_df = df.select_dtypes(include=[np.number])
    non_numeric_df = df.select_dtypes(exclude=[np.number])

    def normalize_data(df, interval='s'):
        return df.resample(interval).mean()

    normalized_df = normalize_data(numeric_df, interval)
    resampled_non_numeric_df = non_numeric_df.resample(interval).first()

    final_normalized_df = pd.concat([normalized_df, resampled_non_numeric_df], axis=1)
    
    return final_normalized_df
