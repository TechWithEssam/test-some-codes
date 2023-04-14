import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

def send_otp(request) :
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    email = request.session["email"]
    username = request.session["username"]
    request.session["otp_secret_key"] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session["otp_valid_date"] = str(valid_date)
    print(otp)
    send_mail(
        "verfiycation account",
        f"""
        hello {username} have a nice day your otp verfiy code is {otp}
        """,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,)