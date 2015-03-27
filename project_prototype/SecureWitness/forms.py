from django import forms
from SecureWitness.models import UserProfile
from django.contrib.auth.models import User

class FileUploadForm(forms.Form):
	title = forms.CharField()
	#author = forms.CharField()
	file = forms.FileField(label = "Select a File") 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('admin_status',)
