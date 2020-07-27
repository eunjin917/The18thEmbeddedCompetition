from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Register(models.Model):
    VIN = models.CharField('차대번호(17자리)', max_length=20, unique=True)
    MAC = models.CharField('MAC주소(12자리)', max_length=20, unique=True)
    name = models.CharField('운전자 이름', max_length=20)
    tel = models.CharField('연락처(-포함)', max_length=20, unique=True)

    def __str__(self):
        return self.MAC

class FileUpload(models.Model):
    myfile = models.FileField('파일 업로드')

# class Accident(models.Model):
#     mycar = models.CharField('차대번호(17자리)', max_length=20)
#     time = models.
#     info = models.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, nickname, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
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
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(_('user name'), max_length=30)
    is_superuser = models.BooleanField(_('superuser status'),default=False)
    is_staff = models.BooleanField(_('staff status'),default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email