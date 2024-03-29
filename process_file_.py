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
    
    # Store original column order, excluding 'Datum' and 'Uhrzeit' as they'll be replaced by 'DateTime'
    original_cols = [col for col in df.columns if col not in ['Datum', 'Uhrzeit']]
    
    # Convert 'Datum' and 'Uhrzeit' to datetime and set as index for resampling
    df['DateTime'] = pd.to_datetime(df['Datum'] + ' ' + df['Uhrzeit'], dayfirst=True)
    df.set_index('DateTime', inplace=True)
    df.drop(columns=['Datum', 'Uhrzeit'], inplace=True)  # These are now represented by the index

    # Split DataFrame into numeric and non-numeric for separate processing
    numeric_df = df.select_dtypes(include=[np.number])
    non_numeric_df = df.select_dtypes(exclude=[np.number])

    # Normalize numeric data
    normalized_df = numeric_df.resample(interval_str).mean()

    # Resample non-numeric data by taking the first value
    resampled_non_numeric_df = non_numeric_df.resample(interval_str).first()

    # Combine normalized numeric data with resampled non-numeric data
    final_normalized_df = pd.concat([normalized_df, resampled_non_numeric_df], axis=1)

    # Sort columns based on the original order
    # Adjust for any new columns added during processing if necessary
    final_col_order = [col for col in original_cols if col in final_normalized_df.columns]
    final_normalized_df = final_normalized_df[final_col_order]

    return final_normalized_df
