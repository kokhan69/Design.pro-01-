from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .signals import post_register
from .models import AdvUser

# Валидатор для ФИО (только кириллические буквы, дефис и пробелы)
validate_cyrillic = RegexValidator(
    regex=r'^[А-Яа-яЁё\s-]+$',
    message='Разрешены только кириллические буквы, пробелы и дефис.'
)

# Валидатор для логина (только латиница и дефис)
validate_latin = RegexValidator(
    regex=r'^[a-zA-Z-]+$',
    message='Разрешены только латинские буквы и дефис.'
)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        validators=[validate_latin],
        help_text='Только латиница и дефис.'
    )

    last_name = forms.CharField(
        label='Фамилия',
        validators=[validate_cyrillic],
        help_text='Только кириллица, пробелы и дефис.'
    )

    first_name = forms.CharField(
        label='Имя',
        validators=[validate_cyrillic],
        help_text='Только кириллица, пробелы и дефис.'
    )

    patronymic = forms.CharField(
        label='Отчество',
        validators=[validate_cyrillic],
        help_text='Только кириллица, пробелы и дефис.',
        required=True
    )

    email = forms.EmailField(required=True, label='Адрес электронной почты')

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,
        help_text='Введите тот же самый пароль еще раз для проверки'
    )

    consent = forms.BooleanField(
        label='Я даю согласие на обработку персональных данных',
        required=True,
        error_messages={'required': 'Необходимо согласие на обработку персональных данных.'}
    )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

        if not self.cleaned_data.get('consent'):
            raise ValidationError({'consent': 'Необходимо согласие на обработку персональных данных.'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        post_register.send(RegisterForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'patronymic', 'send_messages')