from django import forms


# def min_len(value):
#     value = str(value)
#     if len(value) < 4:
#         raise forms.ValidationError("Поле должно содержать минимум 4 символа")


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
