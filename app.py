import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt

st.title("Automated Statement Processor")
st.write("Upload your bank statement file to see the spending summary.")

uploaded_file = st.file_uploader("Upload your bank statement Excel file", type=["xlsx"])

df = pd.read_excel(uploaded_file)
st.write("File loaded successfully!")

# Filter CARD_PAYMENT rows
card_payments = df[df['Type'] == 'CARD_PAYMENT'][['Description', 'Amount']]

# Group and sum
summary = card_payments.groupby('Description')['Amount'].sum().abs()

st.write(summary)
    
st.bar_chart(summary)
