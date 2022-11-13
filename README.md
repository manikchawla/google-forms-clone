# google-forms-clone
Minimalistic Google Forms clone built using Django and jQuery.

## Prerequisites
Install dependencies from requirements.txt file
```
pip install -r requirements.txt
```
Start Python SMTP server before starting Django development server
```
python -m smtpd -n -c DebuggingServer localhost:1025
```
Run Django development server
```
python manage.py runserver
```
