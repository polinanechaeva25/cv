from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class Comment(models.Model):

    user_name = models.CharField(verbose_name='имя', max_length=128, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    is_checked = models.BooleanField(verbose_name='подтверждение почты', db_index=True, default=False)
    web_site = models.CharField(verbose_name='название сайта', max_length=36, blank=False)
    comment = models.TextField(verbose_name='комментарий', max_length=254, blank=False)
    photo = models.ImageField(upload_to='comment_photo', blank=True, default='/unknowing/default.svg')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def __str__(self):
        return self.user_name

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class Certificate(models.Model):

    name = models.CharField(verbose_name='Название курса', max_length=128, blank=False)
    short_description = models.CharField(verbose_name='Короткое описание', max_length=254, blank=False)
    add_datetime = models.DateField(verbose_name='Дата прохождения курса', blank=False)
    photo = models.ImageField(upload_to='course_photo', blank=False)

    def __str__(self):
        return self.name
