from django import forms
from .models import Register, FileUpload, User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.forms  import AuthenticationForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['VIN'].widget.attrs.update(
            {'placeholder': '00000000000000000',
             'class': "rg_item"})
        self.fields['MAC'].widget.attrs.update(
            {'placeholder': '000000000000',
             'class': "rg_item"})
        self.fields['name'].widget.attrs.update(
            {'class': "rg_item"})
        self.fields['tel'].widget.attrs.update(
            {'placeholder': '010-0000-0000 또는 000-000-0000',
             'class': "rg_item"},)

    class Meta:
        model = Register
        fields = ['VIN', 'MAC', 'name', 'tel']

class FileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['myfile'].widget.attrs.update(
            {'class': "file_item"})

    class Meta:
        model = FileUpload
        fields = ['myfile']

class UserForm(UserCreationForm):
    email = forms.EmailField(
        label=_('email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email address'),
                'required': 'True',
                'id': 'email',
            }
        )
    )
    nickname = forms.CharField(
        label=_('nickname'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('nickname'),
                'required': 'True',
                'id': 'nickname',
            }
        )
    )
    password1 = forms.CharField(
        label=_('password1'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
                'id': 'password1',
            }
        )
    )
    password2 = forms.CharField(
        label=_('password2'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
                'id': 'password2',
            }
        )
    )


    class Meta:
        model = User
        fields = ['email', 'nickname', 'password1', 'password2']
    
    # def clean_password2(self):
    #     # email = self.cleaned_data.get("email")
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         messages.info(self.request, '이메일이 일치하지 않습니다.')
    #         print("ㄴ하")
    #     return password2
                
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    # error_messages = {
    #     'invalid_login': _(
    #         "Please enter a correct %(username)s and password. Note that both "
    #         "fields may be case-sensitive."
    #     ),
    #     'inactive': _("This account is inactive."),
    # }

    class Meta:
        model = User # 이거 ..?
        fields = ['email', 'password1']

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email and password:
            try:
                self.user_cache = User.objects.get(email=email)
                if password == self.user_cache.password:
                    return self.user_cache
                else:
                    print("비번일치x")
                    messages.info(self.request, '비밀번호가 일치하지 않습니다.')
                    raise self.get_invalid_login_error()
            except ObjectDoesNotExist:
                print("이멜일치x")
                messages.info(self.request, '이메일이 일치하지 않습니다.')
                raise self.get_invalid_login_error()
        return self.cleaned_data