import pandas as pd
import numpy as np

def process_file(uploaded_file, interval: int):
    # Prepare the interval string
    interval_str = f'{interval}s'

    # Determine the file extension
    file_name = uploaded_file.name
    if file_name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, sep=';', decimal=',', skiprows=2, encoding='latin1')
    elif file_name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, skiprows=2)
    else:
        raise ValueError('File type not supported. Please upload a CSV or Excel file.')
    
    # Convert 'Datum' and 'Uhrzeit' to datetime and set as index for resampling
    df['DateTime'] = pd.to_datetime(df['Datum'] + ' ' + df['Uhrzeit'], dayfirst=True)
    df.set_index('DateTime', inplace=True)
    
    # Split DataFrame into numeric and non-numeric for separate processing
    numeric_df = df.select_dtypes(include=[np.number])
    non_numeric_df = df.select_dtypes(exclude=[np.number])

    # Normalize numeric data
    normalized_df = numeric_df.resample(interval_str).mean()

    # Resample non-numeric data by taking the first value
    resampled_non_numeric_df = non_numeric_df.resample(interval_str).first()

    # Combine normalized numeric data with resampled non-numeric data
    final_normalized_df = pd.concat([normalized_df, resampled_non_numeric_df], axis=1)

    # Extract 'Datum' (Date) and 'Uhrzeit' (Time) from the 'DateTime' index
    final_normalized_df['Datum'] = final_normalized_df.index.date
    final_normalized_df['Uhrzeit'] = final_normalized_df.index.time

    # Define the final column order including 'Datum' and 'Uhrzeit'
    # final_cols = ['Datum', 'Uhrzeit'] + [col for col in df.columns if col not in ['Datum', 'Uhrzeit', 'DateTime']]
    final_cols = ['Datum', 'Uhrzeit', 'DateTime'] + ["DS1 mA", "DS2 mA", "IDM mA", "DDS1 mA", "DDS2 mA", "DSEWS mA", "DDS1 Ausg.Wert", "DDS1 Beiwert", "DDS1 Druck (bar)", "DDS2 Ausg.Wert", "Druck Verpresspumpe (bar)", "IDM Beiwert", "IDM-Ausg.Wert", "Durchfluss (l/min)", "Gesamtmenge Liter"]
    # Reorder columns based on final_cols, ensuring that only columns present in the DataFrame are included
    final_col_order = [col for col in final_cols if col in final_normalized_df.columns]
    final_normalized_df = final_normalized_df[final_col_order]

    # Keep 'DateTime' as the index
    # No need to reset the index as 'DateTime' is already the index

    return final_normalized_df