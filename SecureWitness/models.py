from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import Group
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    admin_status = models.BooleanField(default=False)

    def __str__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


class Folder(models.Model):
    #id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Group(models.Model):
    #group = models.OneToOneField(Group)
    name = models.CharField(max_length=200, primary_key=True)
    members = models.ManyToManyField(User)
    #reports = models.ManyToManyField(Report)

    def __str__(self):
        return self.name


class Request(models.Model):
    requester = models.CharField(max_length=100, default= '')
    group = models.ForeignKey(Group)

    def __str__(self):
        return str(self.group)


class Report(models.Model):
    #id = models.IntegerField(unique=True) #previously had primary key in here
    title = models.CharField(max_length=300, default = '')
    authorId = models.ForeignKey(UserProfile, blank=True)
    authorName = models.CharField(max_length = 30, default = '', blank = True)
    #folder = models.ForeignKey(Folder, blank=True)
    folder = models.IntegerField(default='0', blank=True)
    user_perm = models.TextField(default='', blank=True)
    group_perm = models.ManyToManyField(Group) #String of groups permitted to access the file
    access_type = models.BooleanField(default=False) #False -> Public file, True -> Private file
    timestamp = models.TextField(default='', blank=True)
    shortDesc = models.TextField(default='', blank=True)
    detailsDesc = models.TextField(default='', blank=True)
    dateOfIncident = models.TextField(default='', blank=True, null = True)
    locationOfIncident = models.TextField(default='', blank=True, null = True)
    keywords = models.TextField(default='', blank=True, null = True)
    
		
    def __str__(self):
        return self.title

    def __str__(self):
        return self.title


class File(models.Model):
    file = models.FileField(upload_to='SecureWitness/', blank=True, default = "", null = True)
    report = models.ForeignKey(Report)
    fileType = models.CharField(default = '', max_length=200)
    
class Key(models.Model):
    file = models.OneToOneField(File, primary_key=True)
    key = models.TextField()
