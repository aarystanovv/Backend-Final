import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'


class UsersLog(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'


def validate_password(password):
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")


def not_empty_username(username):
    if not username:
        raise ValidationError("Username is missing.")


def not_empty_email(email):
    if not email:
        raise ValidationError("Email is missing.")


def not_empty_password(password):
    if not password:
        raise ValidationError("Password is missing.")


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
                                validators=[validate_password, not_empty_username, not_empty_email, not_empty_password],
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not username or not email or not password1 or not password2:
            raise forms.ValidationError('Please enter both username and email and passwords.')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def validate_unique_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

    def validate_form_fields(form, error_messages):
        for field_name in form.fields:
            field_value = form.cleaned_data.get(field_name)
            if field_value in (None, '', [], ()):
                error_messages[field_name] = (f"{field_name.capitalize()} field is required.")
        if error_messages:
            raise ValidationError(error_messages)

    def register(request):
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                subject = 'Welcome to My Site'
                message = f'Thank you for registering, {user.username}!'
                from_email = 'ttt.arystan@gmail.com'
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return redirect('registration_success')
        else:
            form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form': form})


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "name",
            "star",
            "price",
            "foto",
        ]

class contactformemail(forms.Form):
    fromemail = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "title",
            "selling_price",
            "discounted_price",
            "description",
            "composition",
            "prodapp",
            "category",
            "product_image",
        ]


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
                                validators=[validate_password, not_empty_username, not_empty_email, not_empty_password],
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not username or not email or not password1 or not password2:
            raise forms.ValidationError('Please enter both username and email and passwords.')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def validate_unique_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

    def validate_form_fields(form, error_messages):
        for field_name in form.fields:
            field_value = form.cleaned_data.get(field_name)
            if field_value in (None, '', [], ()):
                error_messages[field_name] = (f"{field_name.capitalize()} field is required.")
        if error_messages:
            raise ValidationError(error_messages)

    def register(request):
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                subject = 'Welcome to My Site'
                message = f'Thank you for registering, {user.username}!'
                from_email = 'ttt.arystan@gmail.com'
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return redirect('registration_success')
        else:
            form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form': form})



class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus ': 'True',
                                                           'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                          {'autocomplete': 'current-password',
                                                           'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError('Please enter both username and password.')

    def validate_login_credentials(username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Invalid login or password.')

    def login_view(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                try:
                    request.validate_login_credentials(username, password)
                except ValidationError as e:
                    form.add_error(None, e)
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})