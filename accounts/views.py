from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib import messages
from django.contrib.auth import login , logout, authenticate
from .forms import UserCreationForm, LoginForm, CustomPasswordResetForm,CustomSetPasswordForm
from .utils import send_otp
from datetime import datetime
import pyotp
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView


# Create your views here.

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView


class PasswordResetView(FormView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    def form_valid(self, form):
        form.save(
            domain_override='example.com',
            use_https=self.request.is_secure(),
            email_template_name=self.email_template_name,
            request=self.request,
        )
        messages.success(self.request, 'Password reset email has been sent.')
        return super().form_valid(form)


class PasswordResetDoneView(TemplateView):
    template_name = 'accounts/password_reset_done.html'







class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class = CustomSetPasswordForm


class PasswordResetCompleteView(TemplateView):
    template_name = 'accounts/password_reset_complete.html'













def login_form_view(request) :
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() :
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username)
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request, user)
                return redirect("products:home")
            else :
                messages.error(request, "email or password is wrong")
    else :
        form = LoginForm()
    context = {
        "l_form" : form
    }
    return render(request, "accounts/authentications.html", context)


def register_view(request) :
    template_name = "accounts/authentications.html"
    form = UserCreationForm(request.POST or None)
    if form.is_valid() :
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email = user.email
        request.session["email"] = email
        request.session["username"] = user.username
        send_otp(request)
        return redirect("accounts:otp")   
    context = {
        "r_form" : form
    }
    return render(request, template_name, context)


def otp_message_view(request) :
    email = request.session.get("email")
    if email :
        erorr_message = None
        if request.method == "POST" :
            otp = request.POST.get("otp")
            email = request.session["email"]
            otp_secret_key = request.session["otp_secret_key"]
            otp_valid_date = request.session["otp_valid_date"]
            if otp_secret_key and otp_valid_date:
                valid_date = datetime.fromisoformat(otp_valid_date)
                if valid_date > datetime.now() :
                    totp = pyotp.TOTP(otp_secret_key, interval=300)
                    if totp.verify(otp) :
                        user = get_object_or_404(User, email=email)
                        user.is_active = True
                        user.is_verified = True
                        user.save()
                        login(request, user)
                        del request.session["otp_valid_date"]
                        del request.session["otp_secret_key"]
                        del request.session["email"]
                        del request.session["username"]
                        return redirect("/")
                    else :
                        erorr_message = "invalid your one time password".title()
                else :
                    erorr_message = "one time password has expired".title()
            else :
                erorr_message = "ups...something went wrong :(".capitalize()
    else :
        return redirect("products:not_found")
    context = {
        "erorr_message" : erorr_message
    }
    return render(request, "accounts/otp.html", context)


def resend_message(request) :
    email = request.session["email"]
    if email :
        if request.method == "GET" :
            resend = request.GET.get("resend")
            send_otp(request)
            return redirect(request.META.get('HTTP_REFERER'))
    else :
        return redirect("products:not_found")

def logout_view(request) :
    template_name = "accounts/logout.html"
    if request.method == "POST" :
        logout(request)
        return redirect("accounts:login")
    context = {
        "logout":f"{str(request.user.username).upper()}"
    }
    return render(request, template_name, context)