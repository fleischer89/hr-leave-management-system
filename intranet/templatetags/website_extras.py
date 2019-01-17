__author__ = 'Paul Fleischer'


from django import template
# from intranet.models import Comment
from datetime import datetime, date
import time


register = template.Library()

COUNTRIES = dict(Ghana="Ghana", Nigeria="Nigeria", USA="United States of America")


@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplication Filter"""
    return value * arg


@register.filter(name='money_format')
def money_format(value):
    """Multiplication Filter"""
    return "{0:,.2f}".format(round(value, 2))


@register.filter(name='format_address')
def format_address(value):
    return "<br/>".join([v for v in value.split("\n")])


@register.filter(name='upper_case')
def upper_case(value):
    val = value
    if not isinstance(value, str):
        val = value.strftime("%H:%m:%S")
    return val.upper()


@register.filter(name='available_products')
def available_products(products):
    count = 0
    for product in products:
        count += product.quantity
    return count


@register.filter(name='series_data')
def get_series_data(list_values):
    list_dates = dict()
    for value in list_values:
        if value.date in list_dates.keys():
            list_dates[value.date] += 1
        else:
            list_dates[value.date] = 1
    return [v for v in list_dates.values()]


@register.filter(name='first_date')
def get_first_date(list_values):
    return list_values[0].date.strftime("%Y-%m-%d") if len(list_values) > 0 else 0


@register.filter(name='full_name')
def get_full_name(user):
    if user is not None:
        if user.first_name is not None and user.last_name is not None:
            return user.first_name + " " + user.last_name
        if user.first_name is not None:
            return user.first_name
        if user.last_name is not None:
            return user.last_name
    else:
        return user


@register.filter(name='business_owners')
def get_business_owners(member):
    if member is not None:
        return " and " + member
    else:
        return ""


@register.filter(name='photo')
def get_photo(user):
    return user.photo.document.name if user.photo is not None else "photographs/avatar_error.jpg"


@register.filter(name='subtract')
def subtract(value, val):
    return value - val


@register.filter(name='product_name')
def product_name(value):
    product = value.name
    if value.variation is not None:
        product += " - " + value.variation
    return product


@register.filter(name='product_price')
def product_price(value):
    product = 0
    if value is not None:
        product += value
    return product


@register.filter(name='generate_name')
def generate_name(value, label):
    return label.replace('_1', '_' + str(value))


@register.filter(name='month_index')
def month_index(value):
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10, 'November': 11, 'December': 12}
    return months[value]


@register.filter(name='total_sales_amount')
def total_sales_amount(sales):
    amount = 0
    for sale in sales:
        amount += sale.amount
    return amount


@register.filter(name='total_orders_amount')
def total_orders_amount(orders):
    amount = 0
    for order in orders:
        amount += order.invoice.total_price
    return amount


@register.filter(name='normalize_number')
def normalize_number(number):
    return number if number is not None else "-"


@register.filter(name='timestamp')
def get_timestamp(test):
    return time.time()


# @register.filter(name='comment_count')
# def comment_count(post):
#     comments = Comment.objects.filter(post=post)
#     count = len(comments)
#     if count == 0:
#         text = "No comments"
#     elif count == 1:
#         text = "1 comment"
#     else:
#         text = "%s comments" % count
#     return text
#

@register.filter(name='format_date')
def format_date(time=False):
    """
    Get a datetime object or an int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    :param date:
    :param time:
    :return:
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time.replace(tzinfo=None)
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return "%s seconds ago" % second_diff
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return "%s minutes ago" % (second_diff / 60)
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return "%s hours ago" % (second_diff / 3600)
        return ""
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return "%s days ago" % day_diff
    if day_diff < 31:
        return "%s weeks ago" % (day_diff / 7)
    if day_diff < 365:
        return "%s months ago" % (day_diff / 30)
    return "%s years ago" % (day_diff / 365)


@register.filter(name='count')
def get_count(items):
    return len(items)


@register.filter(name='attribute')
def get_attribute(employee, key):
    value = None
    if key is not None:
        if key == 'first_name':
            value = employee.first_name
    return value


@register.filter(name='photo')
def get_photo(photo):
    return photo if photo is not None and len(photo) > 0 else photo


@register.filter(name='get_countries')
def get_countries(name):
    return COUNTRIES[name]


@register.filter(name='format_date')
def reformat_date(value, format):
    # print type(value)
    return value.strftime(format) if value is not None and type(value) == date else value


@register.filter(name='get_country_name')
def get_country_name(country):
    return country.value


def get_all_countries():
    return COUNTRIES.keys()


@register.filter(name='get_short_description')
def get_short_description(description):
    return description[:200] + " ..."



