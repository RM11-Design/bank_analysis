import pandas as pd
from datetime import datetime
import os
import glob
import matplotlib.pyplot as plt
import csv
import pandas as pd
import cred 
from email.message import EmailMessage
# Keeps connection secure
import ssl
import smtplib


# Retrieves today's date which is then embedded into the csv file name.
the_date = datetime.today().strftime("%b-%y")

# The star means all kind of files will be checked.
folder = glob.glob(cred.file)
latest_file = max(folder, key=os.path.getctime)
# Retrieves the file name using the basename.
print(os.path.basename(latest_file))

the_file_name = (os.path.basename(latest_file))

new_file_name = os.path.join(os.path.dirname(latest_file), f"{the_date} Statement.xlsx")
os.rename(latest_file, new_file_name)

if os.path.exists(new_file_name):
    read_file = pd.read_excel(new_file_name)

    # The folder where the csv file is going to be stored.
    to_be_converted_file = cred.new_file_path

    # Converts DataFrame to csv file
    read_file.to_csv(to_be_converted_file, index=None, header=True)

    df = pd.DataFrame(pd.read_csv(to_be_converted_file))
    # print(df)

total_amount = 0
    
type_of_purchase = pd.read_csv(to_be_converted_file)
card_payment_row = df[(type_of_purchase['Type'] == 'CARD_PAYMENT')][['Description','Amount']]
# print(card_payment_row)

no_of_payments = card_payment_row.groupby(['Description']).sum()
# print(no_of_payments)
     
type_of_purchase = pd.read_csv(to_be_converted_file)
card_payment_row = df[(type_of_purchase['Type'] == 'CARD_PAYMENT')][['Description','Amount']]
# print(card_payment_row)

no_of_payments = card_payment_row.groupby(['Description']).sum().abs()
# print(no_of_payments)

no_of_payments.to_csv('all_transactions.csv',header=None)
  
x = []
y = []

with open('all_transactions.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))

plt.bar(x, y, color = 'g', width = 0.72)
plt.xlabel('Shop')
plt.ylabel('Amount (€)')
plt.title(f'Amount spent on {the_date}')
plt.savefig(cred.file_path_to_save_graph,dpi=300)
# Removes the following files after processing.
files_to_remove = ["all_transaction.csv",cred.file_to_remove,f"Statements\\{the_date} Statement.csv"]

email_sender = cred.email_address
# I did this as I didn't want the the code to be displayed in text editor
# "email_key.txt" is assigned to the variable "the_code"
the_code = open("email_key.txt","rt")            
# I assigned the "the_code" file to another variable "email_password"  This reads the "email_key.txt" file.
email_password = the_code.read()
# Finally closes the file.                                                                                                                                                                                                                                                                                                             
the_code.close()                                
email_reciever = cred.email_address 

subject = f"Bank Statement for {the_date}"                  
body = """                   
Here is your bank statement
"""    

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciever
    em["subject"] = subject
    em.set_content(body)
        
    smtp.sendmail(email_sender, email_reciever, em.as_string())
