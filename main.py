import pandas as pd
from datetime import datetime
import os
import glob
import matplotlib.pyplot as plt
import csv
import pandas as pd
import cred 



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

# This opens the csv file and counts the number of times "CARD_PAYMENT" appears
with open(to_be_converted_file,'r') as file:
    data = file.read()
    # Retrieves the keyword i.e. "CARD_PAYMENT" and "TRANSFER"
    no_of_card_payments = data.count("CARD_PAYMENT")
    no_of_transfers = data.count("TRANSFER")

    if "REVERTED":
        new_count = no_of_card_payments + 1
        print("Card Payments: ",new_count)
        print("Number of transfers: ", no_of_transfers)
    else:
        print("Card Payments: ",no_of_card_payments)
        print("Number of transfers: ", no_of_transfers)


# This opens the recently created file and writes "Amount" column into the all_transactions.csv file.
# It iterates through each row in the file and removes the "-" symbol.
# This is done in order to plot the graph properly in Matplotlib.

with open(cred.new_file_path,'r') as file:
    reader = csv.reader(file)
    next(reader)
    with open("all_transaction.csv","w") as transactions:
        writer = csv.writer(transactions)
        total_amount = 0
        for row in reader:
            minus_removed = row[5].strip("-")
            type_of_transaction = row[0]
            all_amounts = float(minus_removed) 
            writer.writerow([type_of_transaction,all_amounts])        
            total_amount += all_amounts 
            print("Total Amount",total_amount,type_of_transaction)
            
card = 0
transfer = 0

with open("all_transaction.csv", 'r') as file:
    data = file.read()
    for line in data.splitlines():
        if "CARD_PAYMENT" in line:
            card += float(line.split(",")[1])
        elif "TRANSFER" in line:
            transfer += float(line.split(",")[1])

print("Card payment total:", card)
print("Transfer total:", transfer)

x = ["Card Payments"," Bank Transfers"]
y = card,transfer

plt.title(f"{the_date} Graph")
plt.xlabel('Transaction Type')
plt.ylabel('Amount (€)')

plt.bar(x,y)
plt.savefig(cred.file_path_to_save_graph,dpi=300)
# plt.show()

# Removes the following files after processing.
files_to_remove = ["all_transaction.csv",cred.file_to_remove,f"Statements\\{the_date} Statement.csv"]

for i in files_to_remove:
    os.remove(i)

