from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from geopy.distance import geodesic

def send_email(current_site,user,name=None,mess="confirm your registration",link="activate",subj = "Activate your account."):
    mail_subject = subj
    if name is None:
        name=user.email
    message = render_to_string('Users/acc_active_email.html', {
        'message' : mess,
        'link' : link,
        'user': user,
        'name': name, 
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
    email.send()

def sort_lat(Docs,coords):
    Docs = sorted(Docs, key=lambda doc : dist((doc.lat,doc.lon),coords))
    print(Docs)
    return Docs

def dist(c1,c2):
    print(c1,geodesic(c1, c2).meters)
    return(geodesic(c1, c2).meters)  
    
