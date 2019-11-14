from registration.forms import RegistrationForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput


class UserForm(RegistrationForm):
    
    username = forms.CharField(label=_("Username"), 
                               max_length=254,
                               widget=forms.TextInput(
                                    attrs={'placeholder': 'Enter username','class':'required form-control'})
                               )
    email = forms.EmailField(label=_("Email"), 
                             max_length=254,
                             widget=forms.TextInput(
                                attrs={'placeholder': 'Enter email','class':'required form-control'})
                             )
    password1 = forms.CharField(label=_("Password"), 
                               widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password','class':'required form-control'})
                               )
    password2 = forms.CharField(label=_("Repeat Password"), 
                               widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password again','class':'required form-control'})
                               )
    
    bad_domains = ['guerrillamail.com']
    
    def clean_email(self):
        email_domain = self.cleaned_data['email'].split('@')[1]
        if User.objects.filter(email__iexact=self.cleaned_data['email'],is_active=True):
            raise forms.ValidationError(_("This email address is already in use."))        
        elif email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using %s email addresses is not allowed. Please supply a different email address." %email_domain))
        return self.cleaned_data['email']
    
    min_password_length = 6
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < self.min_password_length:
            raise forms.ValidationError("Password must have at least %i characters" % self.min_password_length)
        else:
            return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
        
    min_username_length = 6

    def clean_username(self):
        username = self.cleaned_data['username']
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        elif len(username) < self.min_username_length:
            raise forms.ValidationError("Username must have at least %i characters" % self.min_password_length)
        else:
            return self.cleaned_data['username']  


class RegForm(RegistrationForm):

    bad_domains = ['guerrillamail.com']

    def clean_email(self):
        email_domain = self.cleaned_data['email'].split('@')[1]
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use."))
        elif email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using %s email addresses is not allowed. Please supply a different email address." %email_domain))
        return self.cleaned_data['email']

    min_password_length = 6

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < self.min_password_length:
            raise forms.ValidationError("Password must have at least %i characters" % self.min_password_length)
        else:
            return password1

    min_username_length = 5

    def clean_username(self):
        username = self.cleaned_data['username']
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        elif len(username) < self.min_username_length:
            raise forms.ValidationError("Username must have at least %i characters" % self.min_password_length)
        else:
            return self.cleaned_data['username']
