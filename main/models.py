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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_lawyer = models.BooleanField(default=False)
    is_curator = models.BooleanField(default=False)
    #group_leader = models.ForeignKey(UserProfile, null=True)
    
    def __str__(self):
        return str(self.user)


class Rule(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    # TODO: само правило
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class CaseType(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Case(models.Model):
    name = models.CharField(max_length=100)
    caseType = models.ForeignKey(CaseType, on_delete=models.CASCADE)
    

class Report(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_to_check')
    templateDocument = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True, related_name='template')
    templateProfile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='template')
    #TODO: поле для содержимого отчёта
