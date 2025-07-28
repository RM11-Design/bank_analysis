import streamlit as st
import pandas as pd
from datetime import datetime
# import matplotlib.pyplot as plt

the_date = datetime.today().strftime("%b-%y")

st.title("Automated Statement Processor")
st.write("Upload your bank statement file to see your spending summary.")

uploaded_file = st.file_uploader("Upload your bank statement Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("File loaded successfully!")
    
    # Filter CARD_PAYMENT rows
    card_payments = df[df['Type'] == 'CARD_PAYMENT'][['Description', 'Amount']] 
              
    # Group and sum
    summary = card_payments.groupby('Description')['Amount'].sum().abs()
    
    # This keeps track of the items that are reimbursed, so that it can be removed later from the graph.
    reimbursed_descriptions = []
    for description, amount in summary.items():
        reimbursed = st.checkbox(f"{description}: €{amount}", key=description)
        if reimbursed == True:
            # Adds the current description to the reimbursed list.
            reimbursed_descriptions.append(description)
            
    filtered_summary = summary.drop(reimbursed_descriptions)

    # st.write(filtered_summary)
    st.title(f"Graph for {the_date}")
    st.bar_chart(filtered_summary)
