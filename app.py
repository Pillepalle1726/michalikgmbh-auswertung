import streamlit as st
from process_file_ import process_file
import pandas as pd
from io import BytesIO


st.title('Michalik GmbH - Datenanalyse')

uploaded_file = st.file_uploader("Datei auswählen (CSV oder Excel)", type=['csv', 'xlsx'])

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    return output.getvalue()


def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')  # Consider setting index=False here as well

if uploaded_file is not None:
    # Process file based on the selected interval
    interval = st.selectbox('Interval auswählen:', ['1s', '2s', '4s'])

    if st.button('Datei bearbeiten'):
        processed_df = process_file(uploaded_file, interval)

        # Show processed DataFrame (you might want to show only a part of it or just confirm it's processed)
        st.write(processed_df)

        # Convert DataFrame to Excel and CSV
        excel_data = to_excel(processed_df)
        csv_data = to_csv(processed_df)
        csv_filename = uploaded_file.name.replace('.csv', '_processed.csv')
        xlsx_filename = uploaded_file.name.replace('.csv', '_processed.xlsx')
        print(xlsx_filename)
        # Excel Download Button
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name=xlsx_filename,
            mime="application/vnd.ms-excel"
        )

        # CSV Download Button
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=csv_filename,
            mime="text/csv"
        )
