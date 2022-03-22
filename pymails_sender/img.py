import smtplib
import json
from socket import gaierror
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

strFrom = 'pydata-team@e4email.net'
# s = 'hilary.akpu@e4email.net',
email_json = r"C:\Users\holar\Downloads\name_email_dict.json"
js = open(email_json, 'r')

strTo = json.load(js)
js.close()

cc = ['hilary.akpu@e4email.net', 'amarachukwu.jonathan@e4email.net', 'isedu.gloria@e4email.net', 'kosisochukwu.asuzu@e4email.net']

strTo = {'akpu': 'akpuchukwuma.h@gmail.com', 'Amara': 'hilary.akpu@e4email.net'}
# 'Amara': 'amarachukwu.jonathan@e4email.net'
for name, emails in strTo.items():
    # emails = self.email_processor.email_cleaner(emails)
    #     # if not self.email_processor.email_checker(emails):
    #     #     print(f"{name}'s email address: {emails} is invalid and has been dropped")
    #     #     continue
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = "Are you joining us Tomorrow at the Abuja Python Developer's Meetup?"
    msgRoot['From'] = strFrom
    msgRoot['To'] = emails
    # msgRoot.preamble = 'Multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # Add body to email
    try:
        # msgText = MIMEText('Alternative plain text message.')
        # msgAlternative.attach(msgText)

        html_script = r"C:\Users\holar\PycharmProjects\pymails\pymails_sender\script.html"
        sp = open(html_script, 'r')
        email_body = sp.read()
        sp.close()

        #     message['Subject'] = self.subject
        # check if introductory string is given (e.g Hello, Hi, Dear, etc.)

        # check for first appearance of string in email body
        index = email_body.index('Hello')
        index = index + len('Hello')
        # add recipient name after introductory word (i.e Hello <recipient name>)
        email_body = email_body[:index] + f' {name}' + email_body[index:]

        body = MIMEText(email_body, 'html')
        msgAlternative.attach(body)

        # Attach
        file_p = r"C:\Users\holar\Downloads\png_20220311_102453_0000.png"
        fp = open(file_p, 'rb')  # Read image
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        receiver_emails = cc + [emails]
        # receiver_emails = emails
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.ehlo()
        server.login(strFrom, 'f60Z&lb^^hTo')
        server.sendmail(strFrom, receiver_emails, msgRoot.as_string())
        print(f'Email sent to {name}: {emails}')
        server.close()
    except(gaierror, ConnectionRefusedError):
        logging.error(f'Failed to connect to the server. Bad connection settings? Not sent to {name}, {emails}')
    except smtplib.SMTPServerDisconnected:
        logging.error(f'Failed to connect to the server. Wrong username/password? Not sent to {name}, {emails}')
    except smtplib.SMTPException as e:
        # if smtp:
        #     logging.error(f'SMTP error occured: Check smtp domain name provided.\nError message: {e}')
        # else:
        #     logging.error(f'SMTP error occured {e} Not sent to {name}, {emails}')
        logging.error(f'SMTP error occured {e} Not sent to {name}, {emails}')

# Create the root message

# msgRoot = MIMEMultipart('related')
# msgRoot['Subject'] = "Are you joining us Tomorrow at the Abuja Python Developer's Meetup?"
# msgRoot['From'] = strFrom
# msgRoot['To'] = strTo
# msgRoot.preamble = 'Multi-part message in MIME format.'
#
# msgAlternative = MIMEMultipart('alternative')
# msgRoot.attach(msgAlternative)
#
# msgText = MIMEText('Alternative plain text message.')
# msgAlternative.attach(msgText)

# html_script = r"C:\Users\holar\PycharmProjects\pymails\pymails_sender\script.html"
# sp = open(html_script, 'r')
# body = MIMEText(sp.read(), 'html')
# sp.close()
# # msgText = MIMEText(body, 'html')
# msgAlternative.attach(body)

# #Attach
# file_p = r"C:\Users\holar\Downloads\png_20220311_102453_0000.png"
# fp = open(file_p, 'rb') #Read image
# msgImage = MIMEImage(fp.read())
# fp.close()

# # Define the image's ID as referenced above
# msgImage.add_header('Content-ID', '<image1>')
# msgRoot.attach(msgImage)

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.ehlo()
# server.login(strFrom, 'Younghil')
# server.sendmail(strFrom, strTo, msgRoot.as_string())
# print('SE/ntttt')
# server.close()
