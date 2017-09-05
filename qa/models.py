from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class QaUser(models.Model):
    """ Users who can create Questions and Answers """
    class Meta:
        db_table = 'user'

    name = models.CharField(max_length=50)
    auth_user = models.ForeignKey(to=User)

    def __str__(self):
        return "{} - {}".format(self.auth_user.id, self.name)


class Question(models.Model):
    """ Questions created by users and if they are private """
    class Meta:
        db_table = 'question'

    title = models.CharField(max_length=200)
    private = models.BooleanField(default=False)
    user = models.ForeignKey(to=QaUser)

    def __str__(self):
        return "{} - {}".format(self.user.name, self.title)


class Answer(models.Model):
    """ Answers to questions answered by users """
    class Meta:
        db_table = 'answer'

    body = models.CharField(max_length=300)
    question_id = models.ForeignKey(to=Question)
    user = models.ForeignKey(to=QaUser)

    def __str__(self):
        return "Q:{} | A:{}".format(self.question_id.title, self.body)


class Tenant(models.Model):
    """ Consumers who can make API calls """
    class Meta:
        db_table = 'tenant'

    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=30)

    def __str__(self):
        return "{} : {}".format(self.name, self.api_key)


class APIHitsLog(models.Model):
    class Meta:
        db_table = 'api_hits_log'

    tenant = models.ForeignKey(to=Tenant)
    path = models.CharField(max_length=100)
    day = models.DateField(default=datetime.now().date())
    hits = models.IntegerField(default=0)