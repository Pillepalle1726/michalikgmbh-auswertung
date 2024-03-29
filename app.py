import streamlit as st
from process_file_ import process_file
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


st.title('Michalik GmbH - Datenanalyse')

uploaded_file = st.file_uploader("Datei auswählen (CSV oder Excel)", type=['csv', 'xlsx'])

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    return output.getvalue()

def to_csv(df):
    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8')

# Initialize a session state to store the processed DataFrame
if 'processed_df' not in st.session_state:
    st.session_state.processed_df = None

if uploaded_file is not None:
    interval = st.number_input('Interval in Sekunden', min_value=1, max_value=60, value=1)
    if st.button('Datei bearbeiten'):
        # Process the file and store the result in the session state
        st.session_state.processed_df = process_file(uploaded_file, interval)
        st.write(st.session_state.processed_df)

        excel_data = to_excel(st.session_state.processed_df)
        csv_data = to_csv(st.session_state.processed_df)
        csv_filename = uploaded_file.name.replace('.csv', '_processed.csv').replace('.xlsx', '_processed.csv')
        xlsx_filename = uploaded_file.name.replace('.csv', '_processed.xlsx').replace('.xlsx', '_processed.xlsx')
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

if 'viz_clicked' not in st.session_state:
    st.session_state.viz_clicked = False

if st.session_state.processed_df is not None and len(st.session_state.processed_df) > 0:
    if st.button('Visualisierung erstellen'):
        # Set the state to indicate that the button has been clicked
        st.session_state.viz_clicked = True

    # Check if the visualization button has been clicked to show the multiselect
    if st.session_state.viz_clicked:
        selected_columns = st.multiselect('Wähle die Spalten für die Visualisierung:', st.session_state.processed_df.columns)
        
        # Proceed with visualization if columns are selected
        if selected_columns:
            # Check if the DataFrame has a DateTime index
            if isinstance(st.session_state.processed_df.index, pd.DatetimeIndex):
                # Use the index directly for plotting
                times = st.session_state.processed_df.index.time
                # Convert times to matplotlib format
                mdates_times = [mdates.date2num(pd.to_datetime(t.strftime('%H:%M:%S'))) for t in times]
                fig, ax = plt.subplots()
                for col in selected_columns:
                    ax.plot(mdates_times, st.session_state.processed_df[col], label=col)
                ax.legend()
                # Use DateFormatter to format the x-axis labels to display only the time in HH:MM:SS format
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                plt.xticks(rotation=45)  # Rotate x-axis labels if needed
                st.pyplot(fig)
            else:
                st.error("Der DataFrame hat keinen DateTime-Index.")