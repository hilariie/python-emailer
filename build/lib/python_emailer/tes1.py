from email_processing import PyMailer
login_details = ['holaryc@gmail.com', 'password']
email_sender = PyMailer('hilary.akpu@e4email.net', login_details, subject='Job Application', message='Find attached my cv')
email_sender.send_email()