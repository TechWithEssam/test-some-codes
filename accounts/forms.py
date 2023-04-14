from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm,SetPasswordForm
from django.core.exceptions import ValidationError

from .models import User


class CustomSetPasswordForm(SetPasswordForm) :
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password1'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"New Password", 'data-toggle': 'password'})
        self.fields['new_password2'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"New Password Confirmation", 'data-toggle': 'password'})
        
   




class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Enter your Email Address'}))



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        if len(password2) > 8 :
            forms.ValidationError('please pick password more than 8')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['email'].label = ''
        self.fields['username'].label = ''
        self.fields['password2'].label = ''
        # self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # self.fields['username'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Username"})
        self.fields['password1'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Password", "data-toggle":"password"})
        self.fields['password2'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Password confirmation", 'data-toggle': 'password'})
        self.fields['email'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Email"})
        self.fields['username'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Username"})


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_admin')


class LoginForm(forms.Form) :
    username = forms.CharField(label="E-mail", widget=forms.EmailInput)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Password", 'data-toggle': 'password'})
        self.fields['username'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Your Email"})
        
   

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
        return email