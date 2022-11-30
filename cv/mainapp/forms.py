import hashlib
import random
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit

from django import forms

from mainapp.models import Comment


class NameForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': "Введите Ваше имя:"}),
                           label='Имя')


class EmailForm(forms.Form):
    email_address = forms.EmailField(max_length=150,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': "Введите Ваш email:"}), label='Email')


class SubjectForm(forms.Form):
    subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': "Введите тему:"}),
                              label='Тема')


class MessageForm(forms.Form):
    message = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '30',
                                                                            'rows': "10",
                                                                            'placeholder': "Введите сообщение:"}),
                              label='Текст')


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user_name', 'email', 'web_site', 'comment', 'photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['user_name'].label = "Имя:"
        self.fields['email'].label = "Email:"
        self.fields['web_site'].label = "Название проекта:"
        self.fields['comment'].label = "Комментарий:"
        self.fields['photo'].label = ""
        self.template = "../static/js/highslide.js"
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('user_name', css_class='form-control', placeholder="Введите Ваше имя:"),
                    css_class='col-md-12 form-group'),
                Div(
                    Field('email', css_class='form-control', placeholder="Введите Ваш email:"),
                    css_class='col-md-12 form-group'),
                Div(
                    Field('web_site', css_class='form-control', placeholder="Введите название проекта:"),
                    css_class='col-md-12 form-group'),
                Div(
                    Field('comment', css_class='form-control', placeholder="Введите комментарий:"),
                    css_class='col-md-12 form-group'),
                Div(
                    Div(
                        Field('photo', id='input__file', css_class='input input__file'),
                        HTML("""
                                     <label for="input__file" class="input__file-button">
                                        <span class="input__file-icon-wrapper"><img class="input__file-icon" src="../static/img/download.png" alt="Выбрать файл" width="25"></span>
                                        <span class="input__file-button-text">Выберите фото</span>
                                     </label>
                                 """),
                        css_class='input__wrapper'),
                    css_class='col-md-12 form-group'),
                Div(
                    Submit('submit', css_class='readmore d-block w-100', value="Оставить комментарий"),
                    css_class='col-md-12 form-group comment-bott'),
                css_class='row'
            )
        )
