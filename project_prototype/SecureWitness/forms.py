from django import forms
from SecureWitness.models import UserProfile, Request, Folder
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


class AddToFolderForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddToFolderForm, self).__init__(*args, **kwargs)
        self.fields['reports'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in Report.objects.filter(authorName=user, folder=0)])    #using id instead of o.title to ensure unique reports


class MakeFolderForm(forms.Form):
    folder_name = forms.CharField(max_length=120)
    class Meta:
        model = Folder
        fields = ('name',)


class ChangeFolderNameForm(forms.Form):
    folder_name = forms.CharField(max_length=120)
    class Meta:
        model = Folder
        fields = ('name',)


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
    
