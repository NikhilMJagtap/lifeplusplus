from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField()
    blood_choices=(('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-'))
    blood_group = models.CharField(choices=blood_choices,max_length=3)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD=[]


class Req(models.Model):
    req_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='req_by')
    req_for = models.ForeignKey(User,on_delete=models.CASCADE,related_name='req_for')
    text = models.TextField()
    is_fulfilled = models.BooleanField(default=False)


