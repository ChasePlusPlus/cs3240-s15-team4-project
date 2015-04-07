from django import forms
from SecureWitness.models import UserProfile
from django.contrib.auth.models import User
from django.forms import widgets

class FileUploadForm(forms.Form):
    title = forms.CharField()
	#author = forms.CharField()
    file1 = forms.FileField(label = "Select a File", required = False)
    file2 = forms.FileField(label = "Select a File", required = False)
    file3 = forms.FileField(label = "Select a File", required = False)
    file4 = forms.FileField(label = "Select a File", required = False)
    file5 = forms.FileField(label = "Select a File", required = False)
    shortDesc = forms.CharField()
    detailsDesc = forms.CharField(widget = forms.Textarea)
    dateOfIncident = forms.CharField(required=False)#these do not need to be populated
    locationOfIncident = forms.CharField(required = False)#these do not need to be populated
    keywords = forms.CharField(required = False)#these do not need to be populated
    user_perm = forms.BooleanField(required = False)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('admin_status',)
