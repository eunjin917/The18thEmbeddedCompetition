from django import forms
from .models import Register, FileUpload, User, UserManager
# from django.utils.translation import ugettext_lazy as _
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
        label='이메일 주소',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'signup_item',
                'placeholder': '            @police.go.kr',
                'required': 'True',
                'id': 'email',
            }
        )
    )
    nickname = forms.CharField(
        label='이름',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'signup_item',
                'required': 'True',
                'id': 'nickname',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'signup_item',
                'placeholder': '8자 이상 입력',
                'required': 'True',
                'id': 'password1',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'signup_item',
                'placeholder': '비밀번호 재입력',
                'required': 'True',
                'id': 'password2',
            }
        )
    )


    class Meta:
        model = User
        fields = ['email', 'nickname', 'password1', 'password2']
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
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
                    # print("비번일치x")
                    messages.info(self.request, '비밀번호가 일치하지 않습니다.')
                    raise self.get_invalid_login_error()
            except ObjectDoesNotExist:
                # print("이멜일치x")
                messages.info(self.request, '이메일 주소가 일치하지 않습니다.')
                raise self.get_invalid_login_error()
        return self.cleaned_data