from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone

import os
import datetime

from quiz.models import QuizzResult

def avatar_upload_to(instance, filename):
    return os.path.join('profile_img', instance.user.username + os.path.splitext(filename)[1])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,unique = True)
    avatar = models.ImageField(upload_to = avatar_upload_to)
    is_baned = models.BooleanField(default = False)
    scores_factor = models.PositiveSmallIntegerField(default = 1)

    def __str__(self):
        return str(self.user)

RANK_CHOICES = (
    ('Academy Student','academy'),
    ('Genin', 'genin'),
    ('Chuunin','chuunin'),
    ('Jounin','jounin'),
    ('ANBU','anbu'),
    ('Sannin','sannin'),
    ('Kage','kage'),
    ('NARUTO','NARUTO')
)

class CustomUser(AbstractUser,models.Model):
    email = models.EmailField(_('email address'),)
    no_social = models.BooleanField(blank = True,null = True)
    total_scores = models.PositiveIntegerField(default = 0)
    rank = models.CharField(max_length = 40, choices = RANK_CHOICES, default = 'Academy Student')
    slug = models.SlugField(max_length = 60, unique = True, null = True)


    def save(self,*args,**kwargs):
        self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)

class FeedbackModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null = True)
    mail_subject = models.CharField(max_length = 150)
    mail_text = models.TextField()
    send_time = models.DateTimeField(default = datetime.datetime.now,null = True, blank = True)

    def __str__(self):
        return self.mail_subject
