__author__ = 'Smart Empire'

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from intranet.models import *
from collections import Counter
from PIL import Image
from datetime import *
from twilio.rest import TwilioRestClient
import requests
import smtplib
import StringIO
import hashlib
import time
import urllib
import os
import random
import json

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ALPHANUMERIC_RANGE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBER_RANGE = '0123456789'
TWILIO_ACCOUNT_SID = "AC841befe1ba977e57c76bf7e3f3f7d909"
TWILIO_AUTH_TOKEN = "f7b8fc14043ee29ebe5fb57eace72a83"
NASARA_API_KEY = "569e6312da155569e6312da1c9"
RANDOM_PASSWORD = "p@ssw0rd1234"


##############################
#   UTILITY VIEW FUNCTIONS   #
##############################
def generate_invoice_number():
    date_string = datetime.today().strftime('%y%m%d')
    random_number = ''.join(random.choice(ALPHANUMERIC_RANGE) for i in range(4))
    return (date_string + random_number).upper()


def generate_customer_id():
    date_string = date.today().strftime('%y%m')
    random_number = ''.join(random.choice(ALPHANUMERIC_RANGE) for i in range(4))
    return 'CU' + (date_string + random_number).upper()


def generate_distributor_id():
    # date_string = date.today().strftime('%y%m')
    # random_number = ''.join(random.choice(ALPHANUMERIC_RANGE) for i in range(4))
    return random.randint(1, 999999999)


def generate_employee_id(count):
    random_number = "%05d" % count
    return 'DV280314' + random_number


def get_assets_data(employee_id, purchase_date, after, before):
    if employee_id is not None:
        employees = Employee.objects.filter(pk=employee_id)
    elif purchase_date is not None:
        if after:
            employees = Employee.objects.filter(purchase_date__gt=purchase_date)
            return employees
        elif before:
            employees = Employee.objects.filter(purchase_date__lt=purchase_date)
            return employees
        employees = Employee.objects.filter(purchase_date=purchase_date)
    else:
        employees = Employee.objects.all()
    return employees


def get_top_member(data):
    counter = Counter([d.custodian for d in data])
    frequencies = [c for c in counter.values()]
    frequencies.sort()
    index = frequencies.index(frequencies[-1])
    return counter.keys()[index]


def rename_user_photo(photo, new_name):
    data = photo.document.name.split("/")
    extension = data[-1].split('.')[-1]
    name = 'photographs/%s.%s' % (new_name, extension)
    new_path = '%s/%s' % (settings.MEDIA_ROOT, name)
    # print photo.document.path
    # print photo.document.name, name
    # print data, settings.MEDIA_ROOT
    photo.document.name = name
    # print photo.document.name
    # photo.document.path = new_path
    os.rename(photo.document.path, new_path)
    photo.save()


def get_past_date(days):
    return date.today() - timedelta(days)


def get_date_map(d):
    return {'year': d.date.year, 'month': d.date.month, 'day': d.date.day}


def generate_multiple_order_email_template(base_url, bulk_order_ids, customer_name):
    obj = open("./notifications/email_multiple_order.html", "r")
    # product_image = base_url + product.image
    base_url = base_url if base_url is not None else settings.BASE_URL
    order_url = "%s/order/bulk/success?bulk_ids=%s" % (base_url, bulk_order_ids)
    email_template = obj.read()
    email_body = email_template.replace("@@order_url@@", order_url).replace("@@customer_name@@", customer_name)
    obj.close()

    obj = open("./notifications/email_multiple_order_send.html", "w")
    obj.write(email_body)
    obj.close()
    return email_body


def generate_order_email_template(base_url, user_id, order_id, customer_name, product, quantity):
    obj = open("./notifications/email_order.html", "r")
    # product_image = base_url + product.image
    order_url = "%s/panel/%s/records/orders/%s" % (base_url, user_id, order_id)
    email_template = obj.read()
    email_body = email_template.replace("@@order_url@@", order_url).replace("@@order_product@@", product)\
                                .replace("@@order_quantity@@", quantity).replace("@@customer_name@@", customer_name)
    obj.close()

    obj = open("./notifications/email_order_send.html", "w")
    obj.write(email_body)
    obj.close()
    return email_body


def generate_distributor_email_template(base_url, user_id, order_id, customer_name, product, quantity):
    obj = open("./notifications/email_order.html", "r")
    # product_image = base_url + product.image
    order_url = "%s/panel/%s/records/orders/%s" % (base_url, user_id, order_id)
    email_template = obj.read()
    email_body = email_template.replace("@@order_url@@", order_url).replace("@@order_product@@", product).replace("@@order_quantity@@", quantity).replace("@@customer_name@@", customer_name)
    obj.close()

    obj = open("./notifications/email_order_send.html", "w")
    obj.write(email_body)
    obj.close()
    return email_body


def send_email_mail_gun():
    url = "https://api.mailgun.net/v3/sandbox9fcacf20388845ba8297277fb015c71b.mailgun.org/messages"
    key = "key-66c83aef5c3dcaaede713b586681b5d3"
    sender = "Paul Fleischer <Spefben89@yahoo.com>"
    recipients = ["fleischer89@gmail.com"]
    subject = "Email Sending with Mail Gun"
    body = "Hello Paul, email sending with mail gun works!!!"

    send_simple_email(url, key, sender, recipients, subject, body)


# Try running this locally.
def send_simple_email(api, key, sender, recipients, subject, body):
    return requests.post(api,
                         auth=("api", key),
                         data={"from": sender,
                               "to": recipients,
                               "subject": subject,
                               "text": body})


def send_email(sender, recipient, subject, preamble, email_content):
    # Create the root message and fill in the from, to, and subject headers
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.preamble = preamble

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    msg_text = MIMEText('This is the alternative plain text message.')
    msg_alternative.attach(msg_text)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msg_text = MIMEText(email_content, 'html')
    msg_alternative.attach(msg_text)
    # This example assumes the image is in the current directory
    # fp = open('/home/paul/fleischer.jpg', 'rb')
    # msg_image = MIMEImage(fp.read())
    # fp.close()
    #
    # # Define the image's ID as referenced above
    # msg_image.add_header('Content-ID', '<image1>')
    # msg.attach(msg_image)

    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP("%s:%s" % (settings.EMAIL_HOST, settings.EMAIL_PORT))
    # smtp.connect(settings.EMAIL_HOST, port=settings.EMAIL_PORT)
    smtp.starttls()
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()


def send_sms_twilio(sender, recipient, message):
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(body=message, from_=sender, to=recipient)


def send_sms_nasara(sender, recipient, message):
    url = "http://sms.nasaramobile.com/api?api_key=%s&sender_id=%s&phone=%s&message=%s!" % (NASARA_API_KEY,
                                                                                            urllib.quote(sender),
                                                                                            recipient,
                                                                                            urllib.quote(message))
    print url
    r = requests.get(url)


def get_asset_custodian_name(tag):
    names = dict()
    names['ADMN'] = "Administration"
    names['SNPO'] = "Senior Pastor's Office"
    names['GNOO'] = "General Overseer's Office"
    names['DPGO'] = "Deputy General Overseer's Office"
    names['MUSC'] = "Music Department"
    names['TECH'] = "Technical Department"
    names['VIDT'] = "Video Team Department"
    names['TRTA'] = "Theatre Arts Department"
    names['PROT'] = "Protocol Department"
    names['BEAU'] = "Beautification Department"
    names['MENM'] = "Men's Ministry"
    names['WMEN'] = "Women's Ministry"
    names['CHLD'] = "Children's Ministry"
    return names[tag]


def get_months():
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
            'November', 'December']


def get_list_of_countries():
    url = "https://restcountries.eu/rest/v1/all"
    countries = dict()
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        for d in data:
            print d['alpha3Code'], d['name']
            countries[d['alpha3Code']] = d['name']
    return countries


def get_range_of_dates(start, end):
    days = (end - start).days
    date_range = list()
    timestamps = list()
    for i in range(days + 1):
        d = (start + timedelta(i)).date()
        date_range.append({'year': d.year, 'month': d.month, 'day': d.day})
        timestamps.append(time.mktime(d.timetuple()))
    return date_range, timestamps


def build_response(response):
    return json.dumps(dict(message='OK', code=0, data=response))

