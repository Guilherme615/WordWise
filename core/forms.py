from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Word, Request

#ajax(first get):
class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('word', 'description')

#registro de usuário
class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['word_req']
    # #função pra impedir o mais de 1 cadastro por cada email.
    # def clean_email(self):
    #     e = self.cleaned_data['email']
    #     if User.objects.filter(email = e).exists():
    #         raise ValidationError("O email {} já está em uso.".format(e))
    #     return e
        

class AddTeacherForm(forms.Form):
    username = forms.CharField(label='Nome de usuário')