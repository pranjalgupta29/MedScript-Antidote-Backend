from django.core.exceptions import ValidationError
from datetime import date

def validate_date(value):
    today = date.today()
    if value < today :
        raise ValidationError(u'%s is not a valid year!' % value)