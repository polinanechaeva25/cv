# Generated by Django 4.1.3 on 2022-11-16 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название курса')),
                ('short_description', models.CharField(max_length=254, verbose_name='Короткое описание')),
                ('add_datetime', models.DateField(verbose_name='Дата прохождения курса')),
                ('photo', models.ImageField(upload_to='course_photo')),
            ],
        ),
    ]
