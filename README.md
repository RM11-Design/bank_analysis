# Statement Snap

app.py version:
A web app where a user uploads their bank statement and creates a vizualation. 
Additionally, it gives users the opportunity to click transactions that have been reimbursed, enabling greater accuracy of their spending.

main.py version:
This script extracts transaction data from a CSV file exported from Revolut (the banking app).
The script then creates a graph which stores it locally on the user's desktop and emails it using an API.

Libraries used: Pandas | Matplotlib | glob | CSV | Smtplib
