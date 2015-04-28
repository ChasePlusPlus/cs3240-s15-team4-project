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
from SecureWitness.models import File, Group, Report, UserProfile, Request, Folder, Comments
from SecureWitness.forms import EmailLinkForm, EmailForm, LeaveGroupForm, RestoreUserForm, SuspendUserForm, AddMemberForm, RemoveMemberForm, FileUploadForm, SearchForm, UserForm, UserProfileForm, ReportUploadForm, AdminUserForm, RequestAccessForm, GrantAccessForm, CreateGroupForm, EditReportForm, AddToFolderForm, ChangeFolderNameForm, MakeFolderForm, RemoveFromFolderForm, CommentForm, AddReportToGroupForm
import datetime
import mimetypes
from django.core.servers.basehttp import FileWrapper
from functools import reduce
from operator import and_, or_
from Crypto.Cipher import DES3
from django.core.mail import send_mail


#class RequestForm(forms.Form):

@login_required
def adminportal(request):
    context = RequestContext(request)
    
    userid = request.user.id
    userprof = UserProfile.objects.get(user_id=userid)
    is_admin = userprof.admin_status
    #NOTE: user profile ID can be different from request.user.id because if add superuser but don't create user profile
    authId = userprof.id
    
    #selects my reports and public reports
    q1 = Report.objects.filter(authorId_id = authId)
    
    q2 = Report.objects.filter(access_type = 0).exclude(authorId_id = authId)
    myreports = q1
    reports = q2
        
    #selects groups that the user is in
    mygroups = Group.members.through.objects.filter(user_id = userid).values_list('group_id', flat=True)
    reportIdList = []
        
    #select the reports associated with each group
    for group in mygroups:
        q4 = Report.group_perm.through.objects.filter(group_id = group).values_list('report_id', flat = True)
        reportIdList.append(q4)
            
    #add the reports that were selected to the query
    for report in reportIdList:
        q5 = Report.objects.filter(title = report)
        reports = reports | q5
            
    #get all the groups saved that the member is not a part of	
    notMyGroups = Group.members.through.objects.exclude(user_id = userid).values_list('group_id', flat=True).distinct()
    request_groups = []
        
    #check to make sure that the groups chosen are not those the user is in (the way the table is set up is every user has own row with table name
    #meaning that groups with the user can still be chosen when another user in same group)
    for group in notMyGroups:
        if group not in mygroups:
            request_groups.append(group)
    
    if request.method == 'POST':
        if 'submitAdmin' in request.POST:
            admin_user_form = AdminUserForm(data=request.POST)
            if admin_user_form.is_valid:
                userID = request.POST['user']
                user = UserProfile.objects.get(id=userID)
                user.admin_status = True
                user.save()
                admin_user_form = AdminUserForm()
                create_group_form = CreateGroupForm()
                suspend_user_form = SuspendUserForm()
                restore_user_form = RestoreUserForm()
            else: #form is not valid
                print (admin_user_form.errors)
        if 'submitGroup' in request.POST:
            create_group_form = CreateGroupForm(data=request.POST)
            if create_group_form.is_valid:
                group = create_group_form.save()
                group.save()
                create_group_form = CreateGroupForm()
                admin_user_form = AdminUserForm()
                suspend_user_form = SuspendUserForm()
                restore_user_form = RestoreUserForm()
            else:
                print(create_group_form.errors)
        if 'submitSuspend' in request.POST:
            suspend_user_form = SuspendUserForm(data=request.POST)
            if suspend_user_form.is_valid:
                userID = request.POST['user']
                user = User.objects.get(id=userID)
                user.is_active = False
                user.save()
                
                subject = "You have been suspended from SecureWitness."
                message = "You have been suspended from SecureWitness by admin " + request.user.username + "."
                from_email = 'securewitness4@gmail.com'
                to_email = [user.email]
                send_mail(subject, message, from_email, to_email, fail_silently = False)
                
                create_group_form = CreateGroupForm()
                admin_user_form = AdminUserForm()
                suspend_user_form = SuspendUserForm()
                restore_user_form = RestoreUserForm()
            else:
                print(suspend_user_form.errors)
        if 'submitRestore' in request.POST:
            restore_user_form = RestoreUserForm(data=request.POST)
            if restore_user_form.is_valid:
                userID = request.POST['user']
                user = User.objects.get(id=userID)
                user.is_active = True
                user.save()
                
                subject = "You have been restored to SecureWitness."
                message = "You have been restored to SecureWitness by admin " + request.user.username + "."
                from_email = 'securewitness4@gmail.com'
                to_email = [user.email]
                send_mail(subject, message, from_email, to_email, fail_silently = False)
                
                create_group_form = CreateGroupForm()
                admin_user_form = AdminUserForm()
                suspend_user_form = SuspendUserForm()
                restore_user_form = RestoreUserForm()
            else:
                print(restore_user_form.errors)
    else: #request method is not POST
        admin_user_form = AdminUserForm()
        create_group_form = CreateGroupForm()
        suspend_user_form = SuspendUserForm()
        restore_user_form = RestoreUserForm()
    all_reports = Report.objects.all()
    all_groups = Group.objects.all()

    context_dict = {'restore_user_form': restore_user_form, 'suspend_user_form': suspend_user_form, 'all_groups': all_groups, 'all_reports': all_reports, 'reports': reports, 'myreports' : myreports,'groups': mygroups, 'admin_user_form': admin_user_form, 'admin_status': is_admin, 'create_group_form': create_group_form}

    return render_to_response('SecureWitness/adminportal.html', context_dict, context)


def index(request):
#need something if not logged in redirect to login page
    #if admin select all of each
    context = RequestContext(request)
    #username = request.user.first_name + " " + request.user.last_name
    HttpResponse(request.user.id)
    if request.user.is_authenticated():

        userid = request.user.id
        userprof = UserProfile.objects.get(user_id=userid)
        is_admin = userprof.admin_status
        #NOTE: user profile ID can be different from request.user.id because if add superuser but don't create user profile
        authId = userprof.id

        #selects my reports and public reports
        q1 = Report.objects.filter(authorId_id = authId)
        q2 = Report.objects.filter(access_type = 0).exclude(authorId_id = authId)
        myreports = q1
        
        reports = q2
        
        #selects groups that the user is in
        mygroups = Group.members.through.objects.filter(user_id = userid).values_list('group_id', flat=True)
        reportIdList = []
        
        #select the reports associated with each group
        for group in mygroups:
            q4 = Report.group_perm.through.objects.filter(group_id = group).values_list('report_id', flat = True)
            reportIdList.append(q4)
            
        #add the reports that were selected to the query
        for report in reportIdList:
            q5 = Report.objects.filter(id = report).exclude(authorId_id = authId)
            reports = reports | q5
        # return HttpResponse(reports)
        # get all the groups saved that the member is not a part of
        notMyGroups = Group.members.through.objects.exclude(user_id = userid).values_list('group_id', flat=True).distinct()
        request_groups = []
        
        # check to make sure that the groups chosen are not those the user is in (the way the table is set up is every user has own row with table name
        # meaning that groups with the user can still be chosen when another user in same group)
        for group in notMyGroups:
            if group not in mygroups:
                request_groups.append(group)

        if is_admin:
            if request.method == 'POST':
                if 'submit_admin' in request.POST:
                    admin_user_form = AdminUserForm(data=request.POST)
                    if admin_user_form.is_valid:
                        userID = request.POST['user']
                        user = UserProfile.objects.get(user_id=userID)
                        user.admin_status = True
                        user.save()
                        admin_user_form = AdminUserForm()

                    else: # form is not valid
                        print (admin_user_form.errors)
                else: # request method is not POST ####new addition
                    admin_user_form = AdminUserForm()

            else: # request method is not POST
                admin_user_form = AdminUserForm()
            all_reports = Report.objects.all()
            all_groups = Group.objects.all()

            context_dict = {'all_groups': all_groups, 'all_reports': all_reports, 'reports': reports, 'myreports':myreports,
                            'groups': mygroups, 'admin_user_form': admin_user_form, 'admin_status': is_admin,
                            'current_user': request.user.username}
            
        else: # user is not admin
           
            context_dict = {'reports': reports, 'myreports': myreports, 'groups': mygroups, 'request_groups': request_groups,
                            'current_user': request.user.username}
            # return HttpResponse(context_dict['myreports'])
        # NEW CODE for folder creation not yet tested
        if request.method == 'POST':
            if 'submit_make_folder' in request.POST:
                make_folder_form = MakeFolderForm(data=request.POST)
                if make_folder_form.is_valid:
                    foldername = request.POST.get('folder_name', False)
                    new_folder = Folder(name=foldername, owner=request.user)
                    new_folder.save()

                else: # form is not valid
                    print (make_folder_form.errors)
            else: # request method is not POST
                make_folder_form = MakeFolderForm()
        else: # request method is not POST
            make_folder_form = MakeFolderForm()

        search_form = SearchForm()
        context_dict = {'search_form': search_form, 'reports': reports, 'myreports':myreports, 'groups': mygroups, 'request_groups': request_groups, 'admin_status': is_admin}

        context_dict['make_folder_form'] = make_folder_form
        my_folders = [val for val in Folder.objects.all() if val.owner == request.user]
        # my_folders = Folder.objects.all(owner=request.user)
        context_dict['my_folders'] = my_folders


        # add report to group function stuff here
        if request.method == 'POST':
            if 'submit_add_report_to_group' in request.POST:
                add_report_form = AddReportToGroupForm(request.user.get_full_name(), userid, data=request.POST)
                if add_report_form.is_valid:
                    groupname = request.POST.get('groups', False)
                    reportid = request.POST.get('reports', False)
                    group = Group.objects.get(name=groupname)
                    report = Report.objects.get(id=reportid)

                    if report not in report.group_perm.all():
                        report.group_perm.add(group)
                        report.save()

                else: # form is not valid
                    print (add_report_form.errors)
            else: # request method is not POST
                add_report_form = AddReportToGroupForm(request.user.get_full_name(), userid)
        else: # request method is not POST
            add_report_form = AddReportToGroupForm(request.user.get_full_name(), userid)

        context_dict['add_report_to_group_form'] = add_report_form

    else:
        context_dict = {}

    return render_to_response('SecureWitness/index.html', context_dict, context)

@login_required
def results(request):
    context = RequestContext(request)
    
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status
    
    context_dict = {'admin_status': is_admin}
    context_dict['as_post'] = False
    
    if request.method == 'POST':
        context_dict['as_post'] = True
        context_dict['f1'] = request.POST['search_field']
        context_dict['f2'] = request.POST['search_field_2']
        context_dict['andor'] = request.POST['and_or']
        query = request.POST['text']
        query2 = request.POST['text_2']
        context_dict['query'] = query
        context_dict['query2'] = query2
        report1 = []
        report2 = []
        if request.POST['search_field'] == "authorName":
            reports = Report.objects.filter(authorName__icontains=query)
        if request.POST['search_field'] == "title":
            reports = Report.objects.filter(title__icontains=query)
        if request.POST['search_field'] == "shortDesc":
            reports = Report.objects.filter(shortDesc__icontains=query)
        if request.POST['search_field'] == "locationOfIncident":
            reports = Report.objects.filter(locationOfIncident__icontains=query)
        if request.POST['search_field'] == "keywords":
            reports = Report.objects.none()
            r1 = Report.objects.all()
            kwq1 = request.POST['text'].strip().split()
            kwqq1 = request.POST['text'].strip().split()
            for report in r1:
                kw1 = report.keywords.strip().split()
                q = Report.objects.get(title = "report")
                for k1 in kwq1:
                    if k1 in kw1:
                        kwqq1.remove(k1)
                if len(kwqq1) == 0:
                    report1.append(report)
        if request.POST['search_field_2'] == "authorName":
            reports2 = Report.objects.filter(authorName__icontains=query2)
        if request.POST['search_field_2'] == "title":
            reports2 = Report.objects.filter(title__icontains=query2)
        if request.POST['search_field_2'] == "shortDesc":
            reports2 = Report.objects.filter(shortDesc__icontains=query2)
        if request.POST['search_field_2'] == "locationOfIncident":
            reports2 = Report.objects.filter(locationOfIncident__icontains=query2)
        if request.POST['search_field_2'] == "keywords":
            reports2 = Report.objects.none()
            r2 = Report.objects.all()
            kwq2 = request.POST['text_2'].strip().split()
            kwqq2 = request.POST['text_2'].strip().split()
            for report in r2:
                kw2 = report.keywords.strip().split()
                for k2 in kwq2:
                    if k2 in kw2:
                        kwqq2.remove(k2)
                if len(kwqq2) == 0:
                    report2.append(report)
        for report in reports:
            report1.append(report)
        for report in reports2:
            report2.append(report)
        if request.POST['and_or'] == "and":
            queried_reports = []
            for report in report1:
                if report in report2:
                    if report not in queried_reports:
                        if report.access_type == False:
                            queried_reports.append(report)
            for report in report2:
                if report in report1:
                    if report not in queried_reports:
                        if report.access_type == False:
                            queried_reports.append(report)      
        if request.POST['and_or'] == "or":
            if request.POST['text'].strip() == "":
                report1 = []
            if request.POST['text_2'].strip() == "":
                report2 = []
            queried_reports = []
            for report in report1:
                if report not in queried_reports:
                    if report.access_type == False:
                        queried_reports.append(report)
            for report in report2:
                if report not in queried_reports:
                    if report.access_type == False:
                        queried_reports.append(report)
            
        context_dict['results'] = queried_reports
    
    search_form = SearchForm()
    context_dict['search_form'] = search_form
    
    return render_to_response('SecureWitness/results.html', context_dict, context)
    


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
            #formattedTitle = titleNoWS.replace(' ', '_')

            # immediate = Random.get_random_bytes(8)
            immediate = 'IMMEDIAT'
            key = request.POST['dechunker']
            while len(key) < 16:
                key += '0'
            #hashing the key
            # key = SHA256.new(key)
            new_Report = Report(authorId = request.user.profile, authorName = name, title = titleNoWS, shortDesc = request.POST['shortDesc'], detailsDesc = request.POST['detailsDesc'], dateOfIncident = request.POST['dateOfIncident'], locationOfIncident = request.POST['locationOfIncident'], keywords = request.POST['keywords'], access_type = request.POST.get('user_perm', False), dechunker=key, timestamp=str(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")), iv=immediate)
            new_Report.save()

           # if 'user_perm' in request.POST is True:

            if 'submit' in request.POST:			
                #return HttpResponseRedirect(reverse('SecureWitness:report', args=(new_Report.title,)))
                return HttpResponseRedirect(reverse('SecureWitness:index'))
                #render(request, 'SecureWitness/reportDetails.html', {'report': new_Report.title})
            elif 'upload' in request.POST:
		        #direct to add files format
                return HttpResponseRedirect(reverse('SecureWitness:FileUpload', args=(new_Report.id,)))
        else:
			#If there is an issue with uploading a file let the user know
            return HttpResponse("Invalid Report Upload details... Please be sure you are filling out the required fields.")
        
    else:
        form = ReportUploadForm()
 
    data = {'form': form}
	#return render(request, 'polls/upload.html', data)
    return render_to_response('SecureWitness/upload.html', data, context_instance=RequestContext(request))


@login_required
def user_settings(request):
    context = RequestContext(request)
    
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status
    
    return render_to_response('SecureWitness/settings.html', {'admin_status': is_admin}, context)


@login_required
def user_portal(request, curr_user):
    
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status
    
    #return HttpResponse(curr_user)
    #curr_user is the user associaetd with the userportal we're currently on
    #use request.session["currentuser"] to get the currently logged in user
    context = RequestContext(request)
    context_dict = {'curr_user': curr_user}
    granted = False
    no_auth = False
    if request.method == 'POST':
        grant_form = GrantAccessForm(curr_user, data=request.POST)
        if grant_form.is_valid():
            selection = grant_form.cleaned_data['group_requests']  #gets selected option
            add_user = User.objects.get(username=curr_user)
            group = Group.objects.get(name=selection)

            context_dict['group'] = group
            members = [g.username for g in group.members.all()]

            granted = True

            if request.user.username in members:
                #validation to check if the current user has the authority to grant the access request
                context_dict['group'] = group
                group.members.add(add_user)   #adding user to group requested works!
                group.save()
                #now to delete the request
                delete_request = Request.objects.get(requester=curr_user, group=group)
                delete_request.delete()
                subject = "You have been granted access to " + group.name + "."
                message = "You have been granted access to " + group.name + " by " + request.user.username + "."
                from_email = 'securewitness4@gmail.com'
                to_email = [add_user.email]
                send_mail(subject, message, from_email, to_email, fail_silently = False)

                context_dict['no_auth'] = no_auth
            else:
                no_auth = True
                context_dict['no_auth'] = no_auth
        else:
            print(grant_form.errors)
    else:
        grant_form = GrantAccessForm(curr_user)
    #context_dict['no_auth'] = False
    context_dict['granted'] = granted
    context_dict['grant_form'] = grant_form
    context_dict['admin_status'] = is_admin
    return render_to_response('SecureWitness/userportal.html', context_dict, context)


@login_required
def request_access(request, usergroup):
    context = RequestContext(request)
    
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status
    
    group_list = Group.objects.all()
    context_dict = {'group_list': group_list, 'admin_status': is_admin}
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
            new_request = Request(requester = request.user.username, group = g)
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

@login_required
def folder(request, curr_folder):
    context = RequestContext(request)
    context_dict = {'curr_folder': curr_folder}
    username = request.user.first_name + " " + request.user.last_name
    add_folder = Folder.objects.get(name=curr_folder)
    context_dict['folder_id'] = add_folder.id
    reports = Report.objects.all().filter(folder=add_folder.id)
    context_dict['folder_reports'] = reports
    folderID = add_folder.id

    if request.method == 'POST':
        if 'submit_add_to_folder' in request.POST:
            add_form = AddToFolderForm(username, data=request.POST)
            if add_form.is_valid():
                selection = add_form.cleaned_data['reports']  #gets selected option
                add_folder = Folder.objects.get(name=curr_folder)
                report = Report.objects.get(id=selection)
                report.folder = add_folder.id
                report.save(force_update=True)
                reports = Report.objects.all().filter(folder=report.folder)
                #reports = [r for r in Report.objects.all(folder=add_folder.id)]
                context_dict['report'] = report
                context_dict['folder_reports'] = reports

                change_form = ChangeFolderNameForm()
                remove_form = RemoveFromFolderForm(username, folderID)

                return HttpResponseRedirect(reverse('SecureWitness:folder', args={curr_folder}))

            else:
                print(add_form.errors)
        elif 'submit_remove_from_folder' in request.POST:
            remove_form = RemoveFromFolderForm(username, folderID, data=request.POST)
            if remove_form.is_valid():
                selection = remove_form.cleaned_data['reports']  #gets selected option
                add_folder = Folder.objects.get(name=curr_folder)
                report = Report.objects.get(id=selection)
                report.folder = 0
                report.save(force_update=True)
                reports = Report.objects.all().filter(folder=report.folder)
                context_dict['report'] = report
                context_dict['folder_reports'] = reports

                add_form = AddToFolderForm(username)
                change_form = ChangeFolderNameForm()
                return HttpResponseRedirect(reverse('SecureWitness:folder', args={curr_folder}))

            else:
                print(remove_form.errors)
        elif 'submit_change_name' in request.POST:
            change_form = ChangeFolderNameForm(data=request.POST)
            if change_form.is_valid():
                new_name = str(request.POST['folder_name'].rstrip())
                new_name.replace(" ", "_")
                add_folder.name = new_name
                add_folder.save()

                remove_form = RemoveFromFolderForm(username, folderID)
                add_form = AddToFolderForm(username)
                return HttpResponseRedirect(reverse('SecureWitness:index'))

            else:
                print(change_form.errors)

        else:
            add_form = AddToFolderForm(username)
            change_form = ChangeFolderNameForm()
            remove_form = RemoveFromFolderForm(username, folderID)
    else:
        add_form = AddToFolderForm(username)
        change_form = ChangeFolderNameForm()
        remove_form = RemoveFromFolderForm(username, folderID)

    context_dict['add_to_folder_form'] = add_form
    context_dict['change_folder_name_form'] = change_form
    context_dict['remove_from_folder_form'] = remove_form
    return render_to_response('SecureWitness/folder.html', context_dict, context)

@login_required
def email(request, usergroup):
    context = RequestContext(request)
    authorId = request.user #gets logged in user
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status
    g = Group.objects.get(name=usergroup)
    context_dict = {'admin_status': is_admin}
    context_dict['group'] = g
    members = [val for val in g.members.all() if val in g.members.all()]
    
    if authorId in members:
        context_dict['loggedin'] = 1 #if logged in user is in the group
    else:
        context_dict['loggedin'] = 0 #if logged in user is not in the group
    
    if 'submitEmail' in request.POST:
        email_form = EmailForm(g, data=request.POST)
        if email_form.is_valid:
            subject = "from " + request.user.username + ": " + request.POST['subject']
            message = request.POST['message']
            from_email = 'securewitness4@gmail.com'
            member = request.POST['members']
            mem = User.objects.get(username = member)
            to_email = [mem.email]
            send_mail(subject, message, from_email, to_email, fail_silently = False)
            context_dict['email_sent'] = True
            context_dict['emailed_to'] = member
        else: #form is not valid
            print (email_form.errors)
    if 'submitEmailGroup' in request.POST:
        email_form = EmailForm(g, data=request.POST)
        if email_form.is_valid:
            subject = "from " + request.user.username + ": " + request.POST['subject']
            message = request.POST['message']
            from_email = 'securewitness4@gmail.com'
            to_email = []
            for mem in members:
                to_email.append(mem.email)
            send_mail(subject, message, from_email, to_email, fail_silently = False)
            context_dict['email_sent'] = True
            context_dict['emailed_to'] = "all members in " + g.name
        else: #form is not valid
            print (email_form.errors)
    email_form = EmailForm(g)
    context_dict['email_form'] = email_form

    return render_to_response('SecureWitness/email.html', context_dict, context)

@login_required
def group(request, usergroup):

    authorId = request.user #gets logged in user
    context = RequestContext(request)
    
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status

    group_list = Group.objects.all()
    context_dict = {'group_list': group_list, 'admin_status': is_admin}
    g = Group.objects.get(name=usergroup)
    context_dict['group'] = g
    comments = Comments.objects.filter(groupId_id = usergroup)
    userprof = UserProfile.objects.get(user_id=request.user.id)
    context_dict['userID'] = userprof.id
    authIdList = []
    #collect all of the usernames associated with the author of each comment
    for comment in comments:
        auth = UserProfile.objects.get(id = comment.authorId_id)
        user = User.objects.get(id = auth.user_id)
        username = user.username
        authIdList.append(username) 
    
    #zip the arrays together so that it is like a dictionary
    context_dict['comments'] = zip(comments, authIdList)
    commentForm = CommentForm()
    context_dict['comment_form'] = commentForm 
    
    if 'submitLeave' in request.POST:
        memb = request.user.username
        membr = User.objects.get(username = memb)
        g.members.remove(membr)
        
        return HttpResponseRedirect(reverse('SecureWitness:index'))

    #context_dict['currUser'] = request.user
    if is_admin:
        if request.method == 'POST':
            if 'submitAdd' in request.POST:
                add_member_form = AddMemberForm(g, data=request.POST)
                if add_member_form.is_valid:
                    m = request.POST['members']
                    mem = User.objects.get(username = m)
                    g.members.add(mem)
                    r = Request.objects.filter(requester = m, group = g)
                    for req in r:
                        req.delete()
                    subject = "You have been granted access to " + group.name + "."
                    message = "You have been granted access to " + group.name + " by admin " + request.user.username + "."
                    from_email = 'securewitness4@gmail.com'
                    to_email = [mem.email]
                    send_mail(subject, message, from_email, to_email, fail_silently = False)
                else: #form is not valid
                    print (add_member_form.errors)
            if 'submitRemove' in request.POST:
                remove_member_form = RemoveMemberForm(g, data=request.POST)
                if remove_member_form.is_valid:
                    m = request.POST['members']
                    mem = User.objects.get(username = m)
                    g.members.remove(mem)
                    subject = "You have been removed from " + group.name + "."
                    message = "You have been removed from " + group.name + " by admin " + request.user.username + "."
                    from_email = 'securewitness4@gmail.com'
                    to_email = [mem.email]
                    send_mail(subject, message, from_email, to_email, fail_silently = False)
                else:
                    print(remove_member_form.errors)
        else: #request method is not POST
            pass

        add_member_form = AddMemberForm(g)
        #commentsForm = CommentsForm()
        remove_member_form = RemoveMemberForm(g)
        context_dict['add_member_form'] = add_member_form
        context_dict['remove_member_form'] = remove_member_form
    
    members = [val for val in g.members.all() if val in g.members.all()]

    if authorId in members:
        context_dict['loggedin'] = 1 #if logged in user is in the group
    else:
        context_dict['loggedin'] = 0 #if logged in user is not in the group

    #go through all Reports and find reports belonging to usergroup
    reports = Report.group_perm.through.objects.filter(group=usergroup).values_list('report', flat=True)
    actual_reports = []
    for r in reports:
        rep = Report.objects.get(id=r)
        actual_reports.append(rep)

    context_dict['reports'] = actual_reports

    context_dict['members'] = members

    request_list = Request.objects.all()
    requests = [val for val in request_list.all() if val.group == g]
    context_dict['requests'] = requests
    #check if the user had already made a request to join the group
    #CHECKING WORKS! if True, won't prompt user to make more requests
    request_already_made = False
    for r in request_list.all():
        if r.requester == request.user.username and r.group == g:
            request_already_made = True
    context_dict['request_already_made'] = request_already_made
    #/end check

    #if request.method == 'POST':
    if 'submit' in request.POST:
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
    
    
    

    context_dict['add_member_form'] = add_member_form
    context_dict['remove_member_form'] = remove_member_form
    
    #return HttpResponse(remove_member_form)
    if authorId in members:
        context_dict['leave_group_form'] = leave_group_form

    return render_to_response('SecureWitness/group.html', context_dict, context)

def encode_url(str):
    return str.replace(' ', '_')

@login_required
def report(request, selectedReport):
    
    userID = request.user.id
    userprof = UserProfile.objects.get(user_id=userID)
    is_admin = userprof.admin_status
    
    #print("looking at report")
    #return HttpResponse ("Looking at report: {0}".format(selectedReport.title))
    context = RequestContext(request)
    report_list = Report.objects.all()
    context_dict = {'report_list': report_list, 'admin_status': is_admin}

    report = Report.objects.get(id=selectedReport)
    context_dict['report'] = report
    if request.user.get_full_name() == report.authorName:
        context_dict['isAuthor'] = 1
    else:
        context_dict['isAuthor'] = 0

    #get files associated with report
    files = File.objects.filter(report_id = selectedReport)
    context_dict['files'] = files

    return render_to_response('SecureWitness/reportDetails.html', context_dict, context)


def encrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)

    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.chunk(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += (' ' * (16 - len(chunk) % 16)).encode()
                out_file.write(des3.encrypt(chunk))


@login_required
def FileUpload(request, reportID):
    # return HttpResponse(reportTitle)
    if request.method == 'POST':
        # if form is valid get file info and add to the database
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            reportSelected = Report.objects.get(id = reportID)
            fileUploaded = request.FILES['file']
            # uploadContent = fileUploaded.read()
            filename = fileUploaded.name
            # uploadPath = file_full_path = "/tmp/{0}".format(filename)+".upload"

            #if reportSelected.access_type:
            if reportSelected.dechunker != "0000000000000000":
                iv = "IMMEDIAT"
                key = reportSelected.dechunker
                des3 = DES3.new(key, DES3.MODE_CFB, iv)
                fileEnc = filename + ".enc"

                with open("media/" + fileEnc, 'wb') as fileEncoded:
                    for chunk in fileUploaded.chunks(8192):
                        if len(chunk) == 0:
                            break
                        elif len(chunk) % 16 != 0:
                            chunk += (' ' * (16 - len(chunk) % 16)).encode()
                            fileEncoded.write(des3.encrypt(chunk))
                        else:
                            fileEncoded.write(des3.encrypt(chunk))
                        fileEncoded.seek(0)

                mimetypes.init()
                mimeType = mimetypes.guess_type(fileUploaded.name)
                fileTypeString = mimeType[0]
                newFile = File(file = fileEnc, report = reportSelected, fileType = fileTypeString)

                newFile.save()

            else:
                mimetypes.init()
                mimeType = mimetypes.guess_type(fileUploaded.name)
                fileTypeString = mimeType[0]
                newFile = File(file = fileUploaded, report=reportSelected, fileType=fileTypeString)
                newFile.save()
        # if 'done then return to index page
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
        
    data = {'form': form, 'reportID': reportID}
	# return render(request, 'polls/upload.html', data)
    return render_to_response('SecureWitness/FileUpload.html', data, context_instance=RequestContext(request))

def editReport(request, reportID):
    # reportTitle2 = reportTitle.replace("_", " ")
    reportSelected = Report.objects.get(id = reportID)
    # reportID = reportSelected.id

    if request.method == 'POST':
		# form that holds the upload file buttons
        form = EditReportForm(request.POST, request.FILES)
        if form.is_valid():
            titleNoWS = request.POST['title'].rstrip()
            # return HttpResponse(reportSelected.title +" = "+ titleNoWS)
            reportSelected.title = titleNoWS
            reportSelected.shortDesc = request.POST['shortDesc']
            reportSelected.detailsDesc = request.POST['detailsDesc']
            reportSelected.dateOfIncident = request.POST['dateOfIncident']
            reportSelected.locationOfIncident = request.POST['locationOfIncident']
            reportSelected.keywords = request.POST['keywords']
            reportSelected.access_type = request.POST.get('user_perm', False)
            reportSelected.timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
            reportSelected.save(force_update = True)

            if 'addFile' in request.POST:
                return HttpResponseRedirect(reverse('SecureWitness:FileUpload', args=(reportSelected.id,)))
            elif 'deleteFile' in request.POST:
                return HttpResponseRedirect(reverse('SecureWitness:DeleteFile', args = (reportID)))
            else:
                return HttpResponseRedirect(reverse('SecureWitness:index'))
    else:
        # insert form values as default to be shown
        files = File.objects.filter(report_id = reportID)
        form = EditReportForm(initial = {'title': reportSelected.title, 'shortDesc': reportSelected.shortDesc, 'detailsDesc': reportSelected.detailsDesc, 'dateOfIncident': reportSelected.dateOfIncident, 'locationOfIncident': reportSelected.locationOfIncident, 'keywords': reportSelected.keywords, 'user_perm': reportSelected.user_perm} )
    
    context_dict = {'reportID': reportID, 'form': form, 'files' : files}
    return render_to_response('SecureWitness/edit.html', context_dict, context_instance=RequestContext(request))


def deleteReport(request, reportID):
    context = RequestContext(request)
    # reportTitle2 = reportTitle.replace("_", " ")
    reportSelected = Report.objects.get(id = reportID).delete()

    return HttpResponseRedirect(reverse('SecureWitness:index'))

def copyReport(request, reportID):
    # return HttpResponse(request.user.profile)
    context = RequestContext(request)
    # reportTitle2 = reportTitle.replace("_", " ")
    reportSelected = Report.objects.get(id = reportID)
    copyOfReport = Report(authorId = reportSelected.authorId, authorName = reportSelected.authorName, title = reportSelected.title + "(copy)", shortDesc = reportSelected.shortDesc, detailsDesc = reportSelected.detailsDesc, dateOfIncident = reportSelected.dateOfIncident, locationOfIncident = reportSelected.locationOfIncident, keywords = reportSelected.keywords, access_type = reportSelected.access_type, timestamp = str(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))
    copyOfReport.save()
    reportUploaded = Report.objects.get(id = copyOfReport.id)
    filesOfReport = File.objects.filter(report_id = reportID)
    
    for files in filesOfReport:
        newFile = File(file = files.file, report = reportUploaded, fileType = files.fileType)
        newFile.save()

    return HttpResponseRedirect(reverse('SecureWitness:index'))


def deleteFolder(request, folderID):
    context = RequestContext(request)
    reports = Report.objects.all().filter(folder=folderID)
    for rep in reports:
        rep.delete()
    reportSelected = Folder.objects.get(id = folderID).delete()

    return HttpResponseRedirect(reverse('SecureWitness:index'))

def deleteFile(request, reportID):
    # files = File.objects.filter(report_id = reportID)
    if request.method == 'POST':
        if 'submit' in request.POST:
            # form = deleteFilesForm(request.POST, request.FILES)
            fileID = request.POST['file']
            deletedFile = File.objects.get(id = fileID).delete()
            # return HttpResponseRedirect(reverse('SecureWitness:index'))
            return HttpResponseRedirect(reverse('SecureWitness:DeleteFile', args=(reportID,)))
        if 'done' in request.POST:
            return HttpResponseRedirect(reverse('SecureWitness:index'))
    else:
        files = File.objects.filter(report_id = reportID)
        # form = deleteFilesForm(reportID)
    context_dict = {'reportID': reportID, 'files':files}
    return render_to_response('SecureWitness/deleteFile.html', context_dict, context_instance=RequestContext(request))

def download(request, fileID):
    # get filename
    file = File.objects.get(id = fileID)
    report = file.report
    #reportassc = Report.objects.get(id = report)
    #if report.access_type:
    filename = file.file.name
    dechunker = report.dechunker # grabbing the key
    iv = report.iv  # stored immediate
    # decrypt dechunker and iv:
    # return HttpResponse(filename)
    type = file.fileType
    # path = "" # Get file path
    # f = file.file.open('rb')
    # wrapper = FileWrapper(f)
    # email here for decryption key if user_perm is true:
    if report.dechunker != "0000000000000000":
        to_email = [request.user.email]
        send_mail((report.title + " decryption key"), 'key: ' + dechunker + " iv= " + iv, 'securewitness4@gmail.com', to_email, fail_silently=False)
    file.file.seek(0)
    wrapper = FileWrapper(file.file)
    response = HttpResponse(wrapper, content_type= type)

    # concatenate filename with this
    response['Content-Disposition'] = 'attachment; filename=' + filename;
   # else:
   #     file.file.seek(0)
   #     wrapper = FileWrapper(file.file)
   #     response = HttpResponse(wrapper, content_type= type)

    return response

def groupComment(request, usergroup):
    if request.method == 'POST':
        # return HttpResponse(request.user.id)
        # userProfile = request.user.profile
        userprof = UserProfile.objects.get(user_id=request.user.id)
        newComment = Comments(comment = request.POST['comment'], groupId_id = usergroup, authorId_id = userprof.id, authorName = request.user.get_full_name(), timestamp = str(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")) )
        newComment.save()
    # return HttpResponse(usergroup)
    # return HttpResponseRedirect(reverse('SecureWitness:group'))
    return HttpResponseRedirect(reverse('SecureWitness:group', args = (usergroup,)))
