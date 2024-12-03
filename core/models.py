from django.db import models
from django.contrib.auth.models import User
#Criando a classe palavra

class Word(models.Model):
    word = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({}), Criado por: {}".format(self.word, self.description, self.user.username)

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    word_req = models.CharField(max_length=50, verbose_name='Word Request')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word_req} - {self.user.username}"
