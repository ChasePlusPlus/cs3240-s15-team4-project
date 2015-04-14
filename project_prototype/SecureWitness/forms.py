from django import forms
from SecureWitness.models import UserProfile, Request, Group, Report
from django.contrib.auth.models import User
from django.forms import widgets
from SecureWitness.models import Report


class RequestAccessForm(forms.Form):
    #request_access = forms.BooleanField(required=True)
    class Meta:
        model = Request
        fields = ('requester', 'group')


class GrantAccessForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(GrantAccessForm, self).__init__(*args, **kwargs)
        self.fields['group_requests'] = forms.ChoiceField(
            choices=[(o.group, str(o)) for o in Request.objects.filter(requester=user)])


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

class AdminUserForm(forms.Form):

    user = forms.ModelChoiceField(queryset=UserProfile.objects.filter(admin_status=False), required=False)
	
class EditReportForm(forms.Form):
    title = forms.CharField()
	#author = forms.CharField()
    shortDesc = forms.CharField()
    detailsDesc = forms.CharField(widget = forms.Textarea)
    dateOfIncident = forms.CharField(required=False)#these do not need to be populated
    locationOfIncident = forms.CharField(required = False)#these do not need to be populated
    keywords = forms.CharField(required = False)#these do not need to be populated
    user_perm = forms.BooleanField(required = False)
    
class CreateGroupForm(forms.ModelForm):
    
    class Meta:
        model = Group
        fields = ('name', 'members')

class SearchForm(forms.Form):

    CHOICES = (('title', 'Title'), ('shortDesc', 'Short Description'), ('locationOfIncident', 'Location of Incident'), ('keywords', 'Keywords'))
    
    search_field = forms.ChoiceField(choices=CHOICES)
    text = forms.CharField()
