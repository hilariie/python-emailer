# py-emailer
py-emailer: python emailing toolkit

## What is it?
py-emailer is a Python package that aids in sending of emails. It is a robust package which aims to cover every aspect of sending emails thereby, making developers code less.

## Typical Usage
```python
from pymails_sender import PyMailer
login_details = ['sender_email', 'password']
email_sender = PyMailer('recipient_data.csv', login_details, subject='Job Application', 'Find attached my cv')
email_sender.send_email(file_path='cv.pdf')

```
## Main Features
Here are some of the things py-emailer does:
* Checks and cleans common errors in email addresses such as space inbetween strings/characters, fullstop at the end of email, etc.
* Checks for valid email address syntax before attempting to send emails
* Reads email content from strings, .html files, or .txt files
* Reads recipient data from string, list, tuple, set, dictionary, .json, and .csv files.
* It attempts to automatically detect the smtp host of the provided sender email address.
* Attaches files to the email. Can also attach all files in a given directory. Can also display files(images) in the email.
* automatically detects the message type of the email(html or plain)
* Includes recipient's name in the email after the provided introductory string(i.e Hello <recipient_name>)

## Where to get it
The source code is hosted on Github: https://github.com/hilariie/py-emailer

And can be installed from Python Package Index(PyPI)

```
pip install py-emailer
```

## Dependencies
This package only makes use of python builtin packages.

## License
[MIT](LICENSE)

## Contributing
Contributions, bug reports and fixes, documentation improvements and enhancements, and ideas are all welcome.

To contribute:
* Fork this repo
* Clone your repo

    `git clone <your repo>`
* Make commit changes

    `git add <changed files>`
    
    `git commit -m "commit message`
* Push changes

    `git push ..`
* Create a pull request