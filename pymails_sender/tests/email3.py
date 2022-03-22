"""
send email reading recip from json file(list) DONE
send email reading recip from json file DONE #
send email reading recip from csv
send email with html content # DONE
send email with txt content #DONE
send email with no names, and attach string_ #DONE
send email with file attachment dir #DONE
send email with file #DONE
send email with cid #DONE
send email with smtp host. #DONE




"""
from email_processing2 import PyMailer
csv = r"C:\Users\holar\Desktop\exp_e4emails\emails\recipients.csv"
login = ['holaryc@gmail.com', 'Younghil']
fn1 = "json_list.json"
fn2 = "json.json"
fn3 = 'email_content.txt'
fn4 = r"C:\Users\holar\PycharmProjects\pymails\pymails_sender\script.html"
att1 = r"C:\Users\holar\Desktop\exp_e4emails\emails\attachments"
att2 = r"C:\Users\holar\Desktop\exp_e4emails\emails\attachments\sample_image.jfif"
x2 = PyMailer(fn2, login, 'Final Test 2', fn4)
print('TEST3.....')
x3 = PyMailer(['akpuchukwuma.h@gmail.com'], login, 'Final Test 3', fn3)
x3.send_email(string_='Hello', smtp='smtp.mail.yahoo.com')
# x3.send_email(string_='Hello', smtp='smtp.gmail.com')
print('Finally TEST5.....')
x2.send_email(file_path=att1, cid_img='image_test')