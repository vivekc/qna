from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    """ Questions created by users and if they are private """
    class Meta:
        db_table = 'question'

    title = models.CharField(max_length=200)
    private = models.BooleanField(default=0)
    user_id = models.ForeignKey(to=User)


class Answer(models.Model):
    """ Answers to questions answered by users """
    class Meta:
        db_table = 'answer'

    body = models.CharField(max_length=300)
    question_id = models.ForeignKey(to=Question)
    user_id = models.ForeignKey(to=User)


class Tenant(models.Model):
    """ Consumers who can make API calls to fetch """
    class Meta:
        db_table = 'tenant'

    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=30)
