from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)



class teacher(models.Model):
    teachername = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Grade(models.Model):
    username = models.CharField(max_length=32)
    subject = models.CharField(max_length=32)
    Grade = models.CharField(max_length=32)





# class student(models.Model):
#     username = models.CharField(max_length=32)
#     subject = models.CharField(max_length=32)
#     Grade = models.CharField(max_length=32)
# class teachers(models.Model):
#     teachername = models.CharField(max_length=32)
#     password = models.CharField(max_length=32)








