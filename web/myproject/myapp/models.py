from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class Device(models.Model):
    VIN = models.CharField('차대번호(17자리)', max_length=20, unique=True)
    MAC = models.CharField('MAC주소(12자리)', max_length=20, unique=True)
    name = models.CharField('운전자 이름', max_length=20)
    tel = models.CharField('연락처(-포함)', max_length=20, unique=True)

    def __str__(self):
        return self.VIN

class FileUpload(models.Model):
    myfile = models.FileField('파일 업로드')

class Accident(models.Model):
    mycar_date = models.CharField('차대번호(17자리)_사고발생시간', max_length=37, unique=True)
    mycar = models.ForeignKey('Device', related_name='mycar', on_delete=models.CASCADE)
    date = models.CharField('사고발생일시', max_length=20)
    othercars = models.ManyToManyField('Device', related_name='othercars', blank=True)
    noregicar = models.CharField('기기등록X차량 mac주소 모음', blank=True, max_length=10000)
    carcount = models.IntegerField('차량수', default=0)

    def __str__(self):
        return self.mycar_date

class UserManager(BaseUserManager):
    def _create_user(self, email, password, nickname, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, nickname, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('이메일', unique=True)
    nickname = models.CharField('이름', max_length=30)
    is_superuser = models.BooleanField('서비스관리자',default=False)
    is_staff = models.BooleanField('수사기관',default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'

    def __str__(self):
        return self.email