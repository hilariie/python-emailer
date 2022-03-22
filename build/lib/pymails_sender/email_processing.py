import re
import csv
import os
import logging
import smtplib
from socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class EmailProcessor:
    def __init__(self):
        pass
    @staticmethod
    def sample():
        pass

    @staticmethod
    def email_cleaner(email_address):
        """
        Tries to correct common mistakes in email addresses
        :param email_address :type string
        :return: corrected email address :type string
        """
        # check for empty email address
        if not email_address:  # This line checks if the variable is empty. Variable may be empty str, list, dict, etc.
            return ''  # Return empty string
        # Remove white space
        email_address = email_address.replace(' ', '')
        # check for full stop at the end of email address
        if email_address[-1] == '.':
            email_address = email_address[:-1]
        # check for numbers in last part of email address (i.e .co2m, .2net, .ng2)
        if re.search(r'\d', email_address.split('.')[-1]):
            i = email_address.split('.')[-1]
            for letters in i:
                if letters.isdigit():
                    # replace numbers with empty string
                    new_i = i.replace(letters, '')
            email_address = email_address.replace(i, new_i)

        return email_address

    @staticmethod
    def email_checker(email_address):
        """
        check for invalid email addresses
        :param email_address: :type string
        :return: True or False :type boolean
        """
        # reg expression used to validate email format
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email_address):
            return True
        else:
            return False

    @staticmethod
    def email_content_file_reader(email_file):
        """
        reads the html/txt file containing email content
        :param email_file directory to file containing email content
        :return: email content :type str
        """
        with open(email_file, 'r') as email_content_file:
            email_content = [contents for contents in email_content_file]
            email_content = ''.join(email_content)
        return email_content

    def recipient_data(self, recipients):
        """
        Get recipient data and return it as list
        :param recipients: receiver email addresses :type set, tuple, list, dict, str, .csv
        :return: recipient data :type list
        """
        if type(recipients) is set:
            # assume set/tuple has just emails
            return list(recipients)
        if type(recipients) is tuple:
            # assume tuple has just emails
            return list(recipients)
        if type(recipients) is list:
            # list should hold just emails
            return recipients
        if type(recipients) is dict:
            # dict should hold names as keys and emails as values
            name = [names for names, _ in recipients.items()]
            email = [emails for _, emails in recipients.items()]
            return [name] + [email]
        if type(recipients) is str:
            # Check if path is given
            file_checker = os.path.splitext(recipients)
            if file_checker[1] == '.csv':
                # check if path is valid
                if not os.path.exists(recipients):
                    raise FileNotFoundError(f"{recipients} doesn't exist")
                print('calling second function\n')
                recipients = self.recipient_csv_reader(recipients)
                return recipients
            # if string, return as list
            elif not file_checker[1]:
                return [recipients]
        else:
            raise TypeError('email_recipient data should be in type: set, tuple, list, dict, str, or path')

    @staticmethod
    def recipient_csv_reader(csv_file):
        """
        Reads recipient data from csv file
        :param csv_file: directory to csv file
        :return: list of recipient name, and/or emails, and/or cc emails
        """
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as recipients:
                reader = csv.reader(recipients)
                # extract recipient data
                recipient_list = [lines for lines in reader]
            if len(recipient_list[0]) == 1:
                print('found just emails')
                # assume single column holds emails
                # return list of email addresses excluding the header
                return [''.join(emails) for emails in recipient_list][1:]
            elif len(recipient_list[0]) >= 2:
                print('name and emails found')
                # assume name and emails are the columns
                # Exclude the headers
                name = [names[0] for names in recipient_list][1:]
                email = [emails[1] for emails in recipient_list][1:]
                try:
                    # check for CC column
                    cc_email = [cc_emails[2] for cc_emails in recipient_list]
                    return [name] + [email] + [cc_email]
                except IndexError:
                    print(f'CC not found in {os.path.split(csv_file)[1]}')
                    return [name] + [email]
        else:
            raise ValueError(f'{csv_file} not found in directory')

    @staticmethod
    def file_attachments(path, message, names=None):
        """
        Attaches all files in a folder to the email message
        :param path: directory to folder containing email attachments
        :param message: email message
        :param names: preferred names of files - defaults to None
        :return:
        """

        if os.path.isdir(path):
            # check if directory is empty
            if not os.listdir(path):
                raise FileNotFoundError(f"Directory : {path} is empty")
            else:
                try:
                    # check if number of names provided and files in directory are equal
                    if len(os.listdir(path)) != len(names):
                        raise ValueError('file names not equal to number of files in directory')
                # Catch TypeError in case names was not given (i.e names is still None)
                except TypeError:
                    pass

                for index, files in enumerate(os.listdir(path)):
                    # get directory for each file
                    files = os.path.join(path, files)

                    with open(files, 'rb') as attachments:
                        part = MIMEApplication(attachments.read())
                    # Try to add file with given name
                    try:
                        part.add_header(
                            "Content-Disposition",
                            f"attachment:; filename = {names[index]}"
                        )
                    except TypeError:
                        part.add_header(
                            "Content-Disposition",
                            f"attachment:; filename = {files}"
                        )
                    # attach file(s) to email message
                    message.attach(part)

    @staticmethod
    def smtp_checker(email_address):
        """
        Checks email and returns appropriate smtp host
        :param email_address: sender email address :type str
        :return: smtp host :type str
        """
        if '@gmail' in email_address:
            return "smtp.gmail.com"
        if '@hotmail' or '@outlook' in email_address:
            return 'smtp-mail.outlook.com'
        if '@yahoo' in email_address:
            return "smtp.mail.yahoo.com"


class PyMailer(object):
    def __init__(self, email_receivers, login, subject, message):
        """
        :param email_receivers: Recipient email address(es) :type tuple, set, list, str or .csv
        :param login: list containing sender email address and password :type list
        :param subject: Subject of the email message :type str
        :param message: Content of email message :type str, .html, or .txt
        """
        self.email_processor = EmailProcessor()
        # extract and process recipient email addresses
        self.email_receivers = self.email_processor.recipient_data(email_receivers)
        # get recipient and cc data as dict and list
        self.recipient_data, self.cc = self.email_receiver_processing()
        self.login = login
        self.subject = subject
        self.message, self.message_type = self.email_body_processing(message)

    def email_receiver_processing(self):
        """
        Checks if email recevier has name, recipient emails and cc emails based on length of email_receivers list
        :return: cc emails as list and dictionary holding recipient names and emails as keys and values
        """
        cc = ''
        if not len(self.email_receivers):
            raise ValueError('Recipient data is empty')
        # check if email_receiver has just recipient email addresses
        elif len(self.email_receivers) == 1:
            recipient_dict = {}
            for index, emails in enumerate(self.email_receivers):
                recipient_dict[index] = emails
        # check if list has name, recipient and cc email addresses
        elif len(self.email_receivers) < 3:
            try:
                recipient_names, recipient_emails, cc = [email_receiver for email_receiver in self.email_receivers]
            except ValueError:
                recipient_names, recipient_emails = [email_receiver for email_receiver in self.email_receivers]
            finally:
                # convert lists to dictionary holding name as key and emails as values
                recipient_dict = {}
                for index, names in enumerate(recipient_names):
                    recipient_dict[names] = recipient_emails[index]
        else:
            raise ValueError(f'Expected list of length 1, 2, 3 got {len(self.email_receivers)} instead')
        return recipient_dict, cc

    def email_body_processing(self, message):
        """

        :param message: Content of email message :type str, .html, or .txt
        :return:
        """
        # check if message is a file(directory)
        if os.path.split(message)[0]:
            # get the extension (i.e .html, .txt, etc.)
            message_type = os.path.splitext(message)[1]
            # extract contents of the file
            message = self.email_processor.email_content_file_reader(message)
        # if message is string, detect if message_type should be .html or .txt
        elif type(message) is str:
            if re.search('html>', message):
                message_type = '.html'
            else:
                message_type = '.txt'
        else:
            raise TypeError(f'email body should be file directory or str. Received type {type(message)}')
        return message, message_type

    def send_email(self, smtp='', file_path='', string_=''):
        """

        :param smtp: smtp host. If left empty, method attempts to detect smtp host from sender email address :type str
        :param file_path: directory to file or folder containing ONLY files to be attached :type os.path
        :param string_: string which recipient name should appear after \
                                e.g string_='hello' email_body='hello <recipient name>'
        """
        sender_email = self.login[0]
        password = self.login[1]
        email_body = self.message
        # if smtp is empty, automatically check sender email address for suitable smtp host to use
        if not smtp:
            smtp = self.email_processor.smtp_checker(sender_email)
        # Loop through each recipients name and email
        message_type = self.message_type
        for name, emails in self.recipient_data.items():
            if type(name) is int:
                name = ''
            emails = self.email_processor.email_cleaner(emails)
            if not self.email_processor.email_checker(emails):
                print(f"{name}'s email address: {emails} is invalid and has been dropped")
                continue
            message = MIMEMultipart('alternative')
            message['FROM'] = sender_email
            message['TO'] = emails
            message['Cc'] = ','.join(self.cc)

            # Add body to email
            try:
                message['Subject'] = self.subject
                # check if introductory string is given (e.g Hello, Hi, Dear, etc.)
                if string_:
                    # check for first appearance of string in email body
                    index = email_body.index(string_)
                    index = index + len(string_)
                    # add recipient name after introductory word (i.e Hello <recipient name>)
                    email_body = email_body[:index] + f' {name}' + email_body[index:]
                # check if message is string
                if message_type == '.txt':
                    message_type = '.plain'
                message.attach(MIMEText(email_body, message_type[1:]))

                # check if there are attachments
                if file_path:
                    # check if file_path is directory to a folder
                    if not os.path.splitext(file_path)[1]:
                        # attach all the files in directory
                        self.email_processor.file_attachments(file_path, message)
                    # if file path to single fie is given, attach file to email
                    else:
                        with open(file_path, 'rb') as attachments:
                            part = MIMEApplication(attachments.read())
                        part.add_header(
                            "Content-Disposition",
                            f"attachment:; filename = {file_path}"
                        )
                        message.attach(part)

                receiver_emails = [self.cc] + [emails]
                server = smtplib.SMTP_SSL(smtp, 465)
                # server.starttls()
                # server.ehlo()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_emails, message.as_string())
                print(f'Email sent to {name}: {emails}')
                server.close()
            except(gaierror, ConnectionRefusedError):
                logging.error(f'Failed to connect to the server. Bad connection settings? Not sent to {name}, {emails}')
            except smtplib.SMTPServerDisconnected:
                logging.error(f'Failed to connect to the server. Wrong username/password? Not sent to {name}, {emails}')
            except smtplib.SMTPException as e:
                if smtp:
                    logging.error(f'SMTP error occured: Check smtp domain name provided.\nError message: {e}')
                else:
                    logging.error(f'SMTP error occured {e} Not sent to {name}, {emails}')
