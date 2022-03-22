from email_processing import PyMailer
import json

email_topic = 'template test'
email_json = r"C:\Users\holar\Downloads\name_email_dict.json"
# file_p = r"C:\Users\holar\Downloads\png_20220311_102453_0000.png"
file_p = r"C:\Users\holar\Desktop\exp_e4emails\emails\attachments"
file_p2 = r"C:\Users\holar\Desktop\exp_e4emails\emails\attachments\sample_image.jfif"
mail_skeleton = r'C:\Users\holar\PycharmProjects\pymails\pymails_sender\script.html'
mailer = PyMailer({'Boss': 'akpuchukwuma.h@gmail.com', 'Akpu': 'hilary.akpu@e4email.net'}, ['holaryc@gmail.com', 'Younghil'], email_topic, mail_skeleton)
mailer.send_email(cid_img='image1', file_path=file_p2)
mailer.send_email(string_='Hello', file_path=file_p)

for index, files in enumerate(os.listdir(path)):
    # get directory for each file
    files = os.path.join(path, files)
    part = MIMEBase('application', 'octet-stream')
    with open(files, 'rb') as attachments:
        part.set_payload(attachments.read())
    encoders.encode_base64(part)
    # Try to add file with given name
    try:
        part.add_header(
            "Content-Disposition",
            "attachment; filename = {}".format(Path(names[index]).name)
        )
    except TypeError:
        part.add_header(
            "Content-Disposition",
            "attachment; filename = {}".format(Path(files).name)
        )
    # attach file(s) to email message
    message.attach(part)