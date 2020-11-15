import string
import random
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django.template import loader, Context

class Quizzes(models.Model):
    quiz = models.CharField(max_length = 50,null = True,blank = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null = True,related_name = "quiz_author")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True,related_name = "dislikes")
    slug = models.SlugField(max_length = 50,blank = True, unique = True)
    image = models.ImageField(upload_to = 'quiz_img', blank = True)
    preview_field = models.TextField(blank = True)
    timer = models.PositiveSmallIntegerField(null = True,blank = True)
    attempt_time = models.PositiveSmallIntegerField(null = True)
    people_passed = models.ManyToManyField('QuizzResult', blank = True)
    questions_count = models.PositiveSmallIntegerField(null = True,blank = True)
    publucation_time = models.DateTimeField(default = datetime.datetime.now,null = True, blank = True)

    def __str__(self):
        return str(self.quiz)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.quiz)
        super(Quizzes, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("preview", kwargs = {"name":self.slug})

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def total_passes(self):
        return self.people_passed.count()


def avatar_upload_to(instance, filename):
    return os.path.join('profile_img','comment ' + instance.user.username  + os.path.splitext(filename)[1])



class Comments(models.Model):
    quizComment = models.ForeignKey(Quizzes, on_delete = models.CASCADE,null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null = True)
    reply = models.ForeignKey('self', null = True,on_delete = models.CASCADE, related_name = "replies", blank = True)
    comment = models.TextField(default = "comment")
    publicationDate = models.DateTimeField()
    user_img = models.CharField(max_length = 250,blank = True, unique = False)
    is_edited = models.BooleanField(default = False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name = "comments_likes")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True,related_name = "comments_dislikes")

    class Meta:
        # sort comments in chronological order by default
        ordering = ('-publicationDate',)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


    def __str__(self):
        return self.comment




class Questions(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete = models.CASCADE, null = True)
    question = models.CharField(max_length = 100, default="question")
    image = models.ImageField(upload_to = 'quiz_img/questions', blank = True)
    is_multiple_answers = models.BooleanField(blank = True)

    def __str__(self):
        return self.question

def avatar_upload_to(instance, filename):
    return os.path.join('quiz_img/game_questions', instance.user.username + os.path.splitext(filename)[1])

class GameQuestions(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete = models.CASCADE, null = True)
    question = models.CharField(max_length = 100, default="question")
    image = models.CharField(max_length = 250,null = True)
    is_multiple_answers = models.BooleanField(blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null = True)
    is_used = models.BooleanField()

    def __str__(self):
        return self.question


class Answers(models.Model):
    quiz_name = models.ForeignKey(Quizzes, on_delete = models.CASCADE,  null = True)
    question_name = models.ForeignKey(Questions, on_delete = models.CASCADE,  null = True)
    answer = models.CharField(max_length = 100, default="answer")
    complete = models.BooleanField(verbose_name = "Correct")

    def __str__(self):
        return self.answer + " - " + str(self.complete)


class QuizzResult(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete = models.CASCADE, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null = True)
    correct_answers = models.PositiveSmallIntegerField()
    scores = models.PositiveSmallIntegerField(null = True)
    duration = models.CharField(max_length = 15, null = True)
    result_link = models.SlugField(max_length = 50,null = True,)
    result_time = models.DateTimeField(default = datetime.datetime.now,null = True)
    is_successfully_passed = models.BooleanField()


    def __str__(self):
        return str(self.duration)


class GameAnswers(models.Model):
    quiz = models.ForeignKey(Quizzes,on_delete = models.CASCADE, null = True)
    quiz_result = models.ForeignKey(QuizzResult, on_delete = models.CASCADE, null = True)
    question_name = models.ForeignKey(GameQuestions, on_delete = models.CASCADE,  null = True)
    answer = models.CharField(max_length = 100, default="answer")
    complete = models.BooleanField(verbose_name = "Correct")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null = True)
    is_used = models.BooleanField()
    is_selected = models.BooleanField()

    def __str__(self):
        return self.answer
