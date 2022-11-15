import profile
from unicodedata import name
from django.shortcuts import render,redirect
from .models import Profile , Skill , Message
from django.contrib.auth import login,authenticate ,  logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . utils import searchProfiles, paginateProfiles
from .forms import CustomUserCreationForm , ProfileForm , SkillForm , MessageForm

def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username= request.POST['username'].lower()
        password= request.POST['password']

        try :
            user= User.objects.get(username=username)
        except :
            messages.error(request,'Username does not exists')
        
        #authenticate function will return user object if exists or none
        user = authenticate(request, username=username,password=password)
        if user is not None :
            login(request, user) #crates session
            #'next' will be passed from some template ...if next present in request it will be routed to that calling page otherwise to 'account'
            # here next received from single project page {%url 'login'%}?next={{request.path}}
            return redirect(request.GET['next'] if next in request.GET else 'account')
        else :
            messages.error(request,'Invalid Username or Password')

    return render(request , 'users\login-register.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page='register'
    form =CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) #to hold data and modify as per requirements
            user.username = user.username.lower()
            user.save()

            messages.success(request,'user created')
            login(request, user)
            return redirect('edit-account')

        else :
            messages.error(request,'Error occurred while registration')

    context = {'page':page,'form': form}
    return render(request , 'users\login-register.html',context)


def profiles(request):
    profiles , search_query = searchProfiles(request)
    #unpacking of returned tuple
    custom_range, profiles = paginateProfiles(request,profiles,3)

    context = {'profiles' : profiles, 'search_query' : search_query,'custom_range':custom_range}
    return render (request , 'users\profiles.html', context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(decription__exact="")
    otherSkills = profile.skill_set.filter(decription="")
    context = {'profile' : profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render (request, 'users\\user-profile.html',context) # \\ to escape unicode \uXXXX error

@login_required(login_url= 'login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile , 'skills' :skills, 'projects' : projects}
    return render (request, 'users\\account.html',context)


@login_required(login_url= 'login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render (request, 'users\profile-form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('account')
    
    context = {'form' : form}
    return render (request, 'users\skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)

    if request.method == 'POST':
        form = SkillForm(request.POST,instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('account')
    
    context = {'form' : form}
    return render (request, 'users\skill_form.html',context)

@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    context={'object':skill}
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('account')
    return render(request, 'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all() #'messages' is related name....same as profile.message_set.all()...but other field uses that hence we have used related name for this.
    unreadCount = messageRequests.filter(is_read = False).count()
    context={'messageRequests':messageRequests , 'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    #message = Message.objects.get(id=pk) this will also work
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    try :
        sender = request.user.profile
    except:
        sender= None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid() :
            message = form.save(commit=False)
            message.sender= sender
            message.recipient = recipient

            if sender :
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            messages.success(request,'Your message was successfully sent')
            return redirect('user-profile', pk = recipient.id)

    context={'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context)