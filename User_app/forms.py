from django import forms
from .models import CustomUser,AdminHOD,Staffs,Students
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    # user_type = forms.ChoiceField(choices=CustomUser.user_type_data)
    
    

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1','password2' ]

        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'form-control bg-dark text-light border-secondary mt-2 mb-3',
                'placeholder':'enter username'
            }),

            'email' : forms.EmailInput(attrs={
                'class' : 'form-control bg-dark text-light border-secondary mt-2 mb-3',
                'placeholder':'enter email'
            }),

            'password' : forms.PasswordInput(attrs={
                'class' : 'form-control bg-dark text-light border-secondary mt-2 mb-3',
                'placeholder':'enter password'
            }),

             'password2' : forms.PasswordInput(attrs={
                'class' : 'form-control bg-dark text-light border-secondary mt-2 mb-3',
                'placeholder':'enter conform password'
            })


            
        }


class Loginform(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    
    