# StackLibrary
A project management system web application for students to manage their B-Tech projects.

## Project # tags:
StackLibrary, PMS, Project Management System, Django, AWS, SendGrid, Python
## Members: 
1. Sudhanshu Jena
2. Tejas Manjrekar
3. Ishan Bhagat
4. Abhishek Jadhav
## Note
### Changes in settings.py
In settings.py, kye and password fields are edited instead of real value for security purposes.

If you are hosting the application, to use email handling works on the app use SendGrid or some other email handling API sites instead of SMTP.

For example, You have to add or change only the following fields in settings.py 

SENDGRID_API_KEY = 'SENDGRID_API_KEY from sendgrid site'

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'

EMAIL_HOST_PASSWORD = SENDGRID_API_KEY

EMAIL_PORT = 587

EMAIL_USE_TLS = True

And in StackLibrary/accounts/views/email_handler.py at line no 25 write your Mail Id.

If you are working on localhost then the given settings.py is sufficient to work on.


