# Generated by Django 3.0.8 on 2020-09-25 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20200925_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.CharField(max_length=20, verbose_name='사고발생일시'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='수사기관'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='서비스관리자'),
        ),
    ]