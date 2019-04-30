from django.db import models
from django.contrib.auth.models import User


class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length = 120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50) #TODO: do not save password

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)
    def __str__(self):
        return '{} Token is  :  {}'.format(self.user,self.token)


# Create your models here.
class Expense(models.Model):
    text=models.CharField(max_length=255)
    date=models.DateTimeField()
    amount=models.BigIntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{} - {}'.format(self.date,self.amount)
        # return self.text


class Income(models.Model):
    text=models.CharField(max_length=255)
    date=models.DateTimeField()
    amount=models.BigIntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{}-{}'.format(self.date,self.amount)

    