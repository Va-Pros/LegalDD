from django.db import models
from django.contrib.auth.models import User

from os import remove

# Create your models here.


class Document(models.Model):
    content_type = models.CharField(max_length=100, default='application/octet-stream')
    """
    TODO: настроить имя файла
    """
    file = models.FileField(upload_to='')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author')
    
    def delete(self, *args, **kwargs):
        remove(file.name)
        super(Document, self).delete(*args, **kwargs)


class Rule(models.Model):
    name = models.CharField(max_length=100)
    # TODO: само правило
    
    def __str__(self):
        return self.name


"""
Все модели ниже оставлены на случай, если они понадобятся. В проекте на данный момент не используются
"""

class Profile(models.Model):
    name = models.CharField(max_length=100)
    rules = models.ManyToManyField(Rule)


class CaseType(models.Model):
    pass


class Case(models.Model):
    name = models.CharField(max_length=100)
    caseType = models.ForeignKey(CaseType, on_delete=models.CASCADE)
    

class Report(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_to_check')
    templateDocument = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True, related_name='template')
    templateProfile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='template')
    #TODO: поле для содержимого отчёта
