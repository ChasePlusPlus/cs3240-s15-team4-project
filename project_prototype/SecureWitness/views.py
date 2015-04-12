from django.shortcuts import render, render_to_response, get_object_or_404
#from SecureWitness.forms import UserForm, UserProfileForm
#from SecureWitness.models import UserProfile, File
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from SecureWitness.forms import FileUploadForm,UserForm, UserProfileForm, ReportUploadForm, AdminUserForm, RequestAccessForm, GrantAccessForm
from SecureWitness.models import File, Group, Report, UserProfile, Request

import datetime


#class RequestForm(forms.Form):


def index(request):
#need something if not logged in redirect to login page
    #if admin select all of each
    context = RequestContext(request)

    if request.user.is_authenticated():
        userID = request.user.id
        userprof = UserProfile.objects.get(user_id=userID)
        is_admin = userprof.admin_status


        userid = request.user.id
        reports = Report.objects.filter(authorId_id = userid)
        #figure out how to know what group they are in
        
		#selects all the groups that the user is in
        groups = Group.members.through.objects.filter(user_id = userid)

        
        if is_admin:
            if request.method == 'POST':
                admin_user_form = AdminUserForm(data=request.POST)
                if admin_user_form.is_valid:
                    userID = request.POST['user']
                    user = UserProfile.objects.get(user_id=userID)
                    user.admin_status = True
                    user.save()
                    admin_user_form = AdminUserForm()
                    
                else: #form is not valid
                    print (admin_user_form.errors)
                
            else: #request method is not POST
                admin_user_form = AdminUserForm()

            context_dict = {'reports': reports, 'groups': groups, 'admin_user_form':admin_user_form, 'admin_status': is_admin}
        
        else: #user is not admin
            #reports = Report.objects.filter()
            groups = Group.objects.all()
            context_dict = {'reports': reports, 'groups': groups}

    else:
        context_dict = {}

    return render_to_response('SecureWitness/index.html', context_dict, context)

def register(request):
    context = RequestContext(request)
    
    #set to False initially. Changes to True when registration succeeds.
    registered = False

    #If HTTP POST, interested in processing form data
    if request.method == 'POST':
        #try to grab info from raw form info.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #hash password then update user object
            user.set_password(user.password)
            user.save()

            #Sort out UserProfile instance
            #Since we need to set the user attribute ourselves, set commit=False.
            #delays saving model until ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True

        else:
            #print problems to terminal and also shown to user
            print (user_form.errors, profile_form.errors)

    #Not HTTP POST, so render form using two ModelForm instances
    #Forms will be blank for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'SecureWitness/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)

def user_login(request):
    context = RequestContext(request)

    #If request is HTTP POST, try to pull out relevant information
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #See if username/password combo is valid
        user = authenticate(username=username, password=password)
        #userID = user.id
        #userprof = UserProfile.objects.get(user_id=userID)
        #useradmin = userprof.admin_status
        
        if user:
            if user.is_active:
                request.session['currentuser'] = username
                login(request, user)
                return HttpResponseRedirect('/SecureWitness/')
            else:
                return HttpResponse("Your Profiles account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    #Request not HTTP POST, so display login form.
    #Scenario most liekly HTTP GET.
    else:
        return render_to_response('SecureWitness/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/SecureWitness/')

@login_required
def uploadView(request):
    if request.method == 'POST':
		#form that holds the upload file buttons
        
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
			#if the form is valid, put the file where it is supposed to go
			
            #new_fileUpload = SampleModel(file = request.FILES['file'])
            #new_fileUpload.save()
			
            User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
            name = request.user.get_full_name()
            titleNoWS = request.POST['title'].rstrip()
            formattedTitle = titleNoWS.replace(' ', '_')
            new_Report = Report(authorId = request.user.profile, authorName = name, title = titleNoWS, shortDesc = request.POST['shortDesc'], detailsDesc = request.POST['detailsDesc'], dateOfIncident = request.POST['dateOfIncident'], locationOfIncident = request.POST['locationOfIncident'], keywords = request.POST['keywords'], user_perm = request.POST.get('user_perm', False), timestamp = str(datetime.datetime.now()))
            new_Report.save()

            if 'submit' in request.POST:			
                #return HttpResponseRedirect(reverse('SecureWitness:report', args=(new_Report.title,)))
                return HttpResponseRedirect(reverse('SecureWitness:index'))
                #render(request, 'SecureWitness/reportDetails.html', {'report': new_Report.title})
            elif 'upload' in request.POST:
		        #direct to add files format
                return HttpResponseRedirect(reverse('SecureWitness:FileUpload', args=(formattedTitle,)))
        else:
			#If there is an issue with uploading a file let the user know
            return HttpResponse("Invalid File Upload details... Please be sure you are filling out the appropriate fields.")
        
    else:
        form = ReportUploadForm()
 
    data = {'form': form}
	#return render(request, 'polls/upload.html', data)
    return render_to_response('SecureWitness/upload.html', data, context_instance=RequestContext(request))


@login_required
def user_settings(request):
    context = RequestContext(request)
    return render_to_response('SecureWitness/settings.html', {}, context)


@login_required
def user_portal(request, curr_user):
    context = RequestContext(request)
    context_dict = {'curr_user': curr_user}
    granted = False
    if request.method == 'POST':
        grant_form = GrantAccessForm(curr_user, data=request.POST)
        if grant_form.is_valid():
            selection = grant_form.cleaned_data['group_requests']  #gets selected option
            add_user = User.objects.get(username=curr_user)
            group = Group.objects.get(name=selection)
            context_dict['group'] = group
            #context_dict['print'] =add_user
            group.members.add(add_user)   #adding user to group requested works!
            group.save()
            #now to delete the request
            delete_request = Request.objects.get(requester=curr_user, group=group)
            delete_request.delete()

            granted = True
        else:
            print(grant_form.errors)
    else:
        grant_form = GrantAccessForm(curr_user)
    context_dict['granted'] = granted
    context_dict['grant_form'] = grant_form
    return render_to_response('SecureWitness/userportal.html', context_dict, context)


@login_required
def request_access(request, usergroup):
    context = RequestContext(request)
    group_list = Group.objects.all()
    context_dict = {'group_list': group_list}
    g = Group.objects.get(name=usergroup)
    context_dict['group'] = g

    requested = False

    #If HTTP POST, interested in processing form data
    if request.method == 'POST':
        #getting data for the only purpose of validation
        request_form = RequestAccessForm(data=request.POST)
        #validation
        if request_form.is_valid():
            #if request_form.request_access == True:
            new_request = Request(requester = request.session["currentuser"], group = g)
            #request_list = Request.objects.all()
            #requests = [val for val in request_list.all() if val.group == g]
            #if request.session["currentuser"] not in requests:
            new_request.save()

            requested = True

        else:
            print(request_form.errors)
    #Not HTTP POST, so render form using two ModelForm instances
    #Forms will be blank for user input
    else:
        request_form = RequestAccessForm()

    return render_to_response('SecureWitness/request.html',{'group': g, 'request_form': request_form, 'requested': requested},context)

def grant_access(request, curr_user):
    pass

@login_required
def group(request, usergroup):
    authorId = request.user #gets logged in user

    context = RequestContext(request)
    group_list = Group.objects.all()
    context_dict = {'group_list': group_list}
    g = Group.objects.get(name=usergroup)
    context_dict['group'] = g
    members = [val for val in g.members.all() if val in g.members.all()]

    if authorId in members:
        context_dict['loggedin'] = 1 #if logged in user is in the group
    else:
        context_dict['loggedin'] = 0 #if logged in user is not in the group

    context_dict['members'] = members

    request_list = Request.objects.all()
    requests = [val for val in request_list.all() if val.group == g]
    context_dict['requests'] = requests
    #check if the user had already made a request to join the group
    #CHECKING WORKS! if True, won't prompt user to make more requests
    request_already_made = False
    for r in request_list.all():
        if r.requester == request.session["currentuser"] and r.group == g:
            request_already_made = True
    context_dict['request_already_made'] = request_already_made
    #/end check

    if request.method == 'POST':
        #getting data for the only purpose of validation
        request_form = RequestAccessForm(data=request.POST)
        #validation
        if request_form.is_valid():
            new_request = Request(requester = request.session["currentuser"], group = g)
            new_request.save()
            requested = True
        else:
            print(request_form.errors)
    else:
        request_form = RequestAccessForm()

    try:
        selected_request = requests[request.POST['choice']]
    except (KeyError, Request.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'SecureWitness/group.html', context_dict)
    else:
        selected_request.requester = "ITWORKED"
        selected_request.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return render(request, 'SecureWitness/group/'+usergroup, context_dict)
        return HttpResponseRedirect(reverse('SecureWitness:group'))

    #request_list = Request.objects.all()
    #requests = [val for val in request_list.all() if val.group == g]
    #context_dict['requests'] = requests

    #context_dict = {'request_list': request_list}
    #r = Request.objects.get(group=usergroup)
    #context_dict['request'] = r
    #requests = [val for val in r.requester.all() if val in r.requester.all()]

    #prints out all requests that have been made to the group  #TODO: change Request model charfield to foreignkey with user, make form in html group to ask for access


    return render_to_response('SecureWitness/group.html', context_dict, context)

def encode_url(str):
    return str.replace(' ', '_')

def report(request, selectedReport):
    #print("looking at report")
    #return HttpResponse ("Looking at report: {0}".format(selectedReport.title))
    context = RequestContext(request)
    report_list = Report.objects.all()
    context_dict = {'report_list': report_list}
	#need to get rid of extra space AND encode url
    #titleRequest = selectedReport.replace('_', ' ')
	#context_dict['titleVal'] = titleRequest
    selectedReport2 = selectedReport.replace("_"," ")
    report = Report.objects.filter(title=selectedReport2)
    context_dict['report'] = report

    #get files associated with report
    files = File.objects.filter(report_id = selectedReport2)
    context_dict['files'] = files
	
	
    return render_to_response('SecureWitness/reportDetails.html', context_dict, context)

def FileUpload(request, reportTitle):
	#return HttpResponse(reportTitle)
    if request.method == 'POST':
        #if form is valid get file info and add to the database
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():            
            #return HttpResponse("VALID")
            reportTitle2 = reportTitle.replace("_", " ")
            reportSelected = Report.objects.get(title = reportTitle2)
            newFile = File(file = request.FILES['file'], report = reportSelected)
            newFile.save()
        #if 'done then return to index page
            if 'done' in request.POST:
                #return HttpResponse("DONE")
                return HttpResponseRedirect(reverse('SecureWitness:index'))
		#if add file pressed then return to file upload page
            elif 'add' in request.POST:
                #return HttpResponse("ADD")
                form = FileUploadForm()
        else:
            return HttpResponse("ELSE")
        
    else:
        form = FileUploadForm()
        
    data = {'form': form, 'reportTitle': reportTitle}
	#return render(request, 'polls/upload.html', data)
    return render_to_response('SecureWitness/FileUpload.html', data, context_instance=RequestContext(request))
    

