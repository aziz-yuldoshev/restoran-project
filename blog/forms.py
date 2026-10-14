from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article

        fields = (
            'title',
            'content',
            'price',
            'photo',
            'category'
        )

        widgets = {

            'title': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Taom nomi'
            }),

            'content': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Tavsif'
            }),

            'price': forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Narxi'
            }),

            'photo': forms.FileInput(attrs={
                'class':'form-control'
            }),

            'category': forms.Select(attrs={
                'class':'form-control'
            })

        }



class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Foydalanuvchi nomi'
        })
    )


    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Parol'
        })
    )



class RegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Login'
        })
    )


    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'Email'
        })
    )


    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Ism'
        })
    )


    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Familiya'
        })
    )


    class Meta:

        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )