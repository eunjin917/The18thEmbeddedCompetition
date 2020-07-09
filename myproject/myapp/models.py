from django.db import models

# Create your models here.

class Register(models.Model):
    VIN = models.CharField('차대번호(17자리)', max_length=17)
    MAC = models.CharField('MAC주소(12자리)', max_length=12)
    name = models.CharField('운전자 이름', max_length=20)
    tel = models.CharField('연락처', max_length=13)


    def __str__(self):
        return self.MAC

class FileUpload(models.Model):
    myfile = models.FileField('파일 업로드')