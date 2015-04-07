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

    

class Report(models.Model):
    #id = models.IntegerField(unique=True) #previously had primary key in here
    title = models.CharField(max_length=300, primary_key=True, default = '')
    authorId = models.ForeignKey(UserProfile, blank=True)
    authorName = models.CharField(max_length = 30, default = '', blank = True)
    #folder = models.ForeignKey(Folder, blank=True)
    #user_perm = models.TextField #String of users permitted to access the file
    user_perm = models.TextField(default='', blank=True)
    group_perm = models.TextField(default='', blank = True) #String of groups permitted to access the file
    access_type = models.BooleanField(default=False) #False -> Public file, True -> Private file
    file1 = models.FileField(upload_to='SecureWitness/', blank=True, default = "", null = True)
    file2 = models.FileField(upload_to='SecureWitness/', blank= True, default = "", null = True)
    file3 = models.FileField(upload_to='SecureWitness/', blank=True, default = "", null = True)
    file4 = models.FileField(upload_to='SecureWitness/', blank=True, default = "", null = True)
    file5 = models.FileField(upload_to='SecureWitness/', blank=True, default = "", null = True)
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
    report = models.ForeignKey(Report)
    
class Key(models.Model):
    file = models.OneToOneField(File, primary_key=True)
    key = models.TextField()
