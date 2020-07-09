from django import forms
from .models import Register, FileUpload

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
            {'placeholder': '000-0000-0000',
             'class': "rg_item"})

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