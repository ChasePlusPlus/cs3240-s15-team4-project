from django import forms
from SecureWitness.models import UserProfile
from django.contrib.auth.models import User
from django.forms import widgets

class ReportUploadForm(forms.Form):
    title = forms.CharField()
	#author = forms.CharField()
    shortDesc = forms.CharField()
    detailsDesc = forms.CharField(widget = forms.Textarea)
    dateOfIncident = forms.CharField(required=False)#these do not need to be populated
    locationOfIncident = forms.CharField(required = False)#these do not need to be populated
    keywords = forms.CharField(required = False)#these do not need to be populated
    user_perm = forms.BooleanField(required = False)
    
class FileUploadForm(forms.Form):
    file = forms.FileField(label = "Select a File", required = False)
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('admin_status',)
