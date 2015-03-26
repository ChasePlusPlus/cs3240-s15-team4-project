from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    admin_status = models.BooleanField(default=False)

    def __str__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


class Folder(models.Model):
    #id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class File(models.Model):
    #id = models.IntegerField(unique=True) #previously had primary key in here
    title = models.CharField(max_length=300, primary_key=True)
    author = models.ForeignKey(User)
    folder = models.ForeignKey(Folder)
    #user_perm = models.TextField #String of users permitted to access the file
    user_perm = models.TextField(default='')
    group_perm = models.TextField(default='') #String of groups permitted to access the file
    access_type = models.BooleanField(default=False) #False -> Public file, True -> Private file

    def __str__(self):
        return self.title


class Key(models.Model):
    file = models.OneToOneField(File, primary_key=True)
    key = models.TextField()
