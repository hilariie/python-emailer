# python-emailer
python-emailer: python emailing toolkit

## What is it?
python-emailer is a Python package that aids in sending of emails. It is a robust package which aims to cover every aspect of sending emails thereby, making developers code less.

## Typical Usage
```python
from python_emailer.email_processing import PyMailer
login_details = ['sender_email', 'password']
email_sender = PyMailer('recipient_data.csv', login_details, subject='Job Application', 'Find attached my cv')
email_sender.send_email(file_path='cv.pdf')

```
## Main Features
Here are some of the things python-emailer does:
* Checks and cleans common errors in email addresses such as space inbetween strings/characters, fullstop at the end of email, etc.
* Checks for valid email address syntax before attempting to send emails
* Reads email content from strings, .html files, or .txt files
* Reads recipient data from string, list, tuple, set, dictionary, .json, and .csv files.
* It attempts to automatically detect the smtp host of the provided sender email address.
* Attaches files to the email. Can also attach all files in a given directory. Can also display files(images) in the email.
* automatically detects the message type of the email(html or plain)
* Includes recipient's name in the email after the provided introductory string(i.e Hello <recipient_name>)

## Where to get it
The source code is hosted on Github: https://github.com/hilariie/python-emailer

And can be installed from Python Package Index(PyPI)

```
pip install python-emailer
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

## How to use
#### File attachments:
___
To attach files, pass in the path to the file.

```python
send_email(file_path='C:\\email\\attachments\\cv.pdf')
```

To attach multiple files, put all files in a directory and pass in the path to that directory in file_path.

```python
send_email(file_path='C:\\email\\attachments')
```

To display images in email, make sure you have cid:<image_name> in your email content/message where you want to display the image.
An example is shown below

```python
Hello, 
    <p>Below is the order of the meetup</p>
    <p>
    <img height="auto" src="cid:image_test" style=".." width="100"/>
    </p>
```

pass in the exact cid value in the send_email method

```python
send_email(cid_img='image_test')
```
___

#### String_:
In a case where you have multiple recipients (names and email addresses) and  you wish to address them by their names, you just have to pass the greeting string.

say email body = "Hello, \nWelcome to web3"

```python
send_email(string_='Hello')
```

email appears as:

`Hello <recipient_name>`

`Welcome to web3`
___

#### Recipient data:
Recipient data can be read from various data and file types such as

* sets - recipient email addresses
* lists - recipient email addresses
* tuples - recipient email addresses
* dictionaries - recipient email addresses, names, and cc
* string - recipient email addresses
* .json files - recipient email addresses, names, and cc
* .csv files - recipient email addresses, names, and cc

##### .csv files:
csv files should be arranged in this order below
![screenshot](csv.png)

##### .json files/dictionaries
Dictionaries should be in one of the two structures
- {names:[name1, name2, ...], emails:[email1, email2, ...], cc:[cc1, cc2, ...]}
- {name1:email1, name2:email2, ...}