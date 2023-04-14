import urllib.request
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# The mail addresses and password
sender_address = 'henrikdchristensen@gmail.com'
sender_pass = 'wjvfdopgtbuxqzbn'
receiver_address = 'henrikdchristensen@gmail.com'

# What to search for?
# space in URL: "%20" e.g. "asus%20rog%20strix"
items = ["PG279QM", "PG32UQX", "PG27UQX"]  # "VG27AQ"
category = "Skærme"

mail_content = ""

for item in items:
    found = False
    mail_content += item + ":\n"

    url = f'https://www.pricerunner.dk/public/search/v2/dk?q=' + item
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    content = json.loads(r.decode('utf-8'))

    if len(content["products"]) != 0:
        for products in content["products"]:
            if str(products["name"]).lower().find(item.lower()) != -1 and \
                    str(products["category"]["name"]).lower().find(category.lower()) != -1:
                found = True
                mail_content += str(products["name"]) + " ; Price: " + \
                    str((products["lowestPrice"]["amount"])) + "\n"

    mail_content += "Nothing found...\n\n" if not found else "\n"

# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'ASUS Monitor'  # subject line

# The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))

# Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
session.starttls()  # enable security
session.login(sender_address, sender_pass)  # login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
