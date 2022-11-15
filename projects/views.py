from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Project , Tag
from django.db.models import Q
from . utils import searchProjects , paginateProjects
from .forms import ProjectForm , ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def projects(request):
    projects, search_query = searchProjects(request)
    
    custom_range, projects = paginateProjects(request,projects,6)
    context = {'projects' : projects, 'search_query':search_query,'custom_range':custom_range}
    return render (request, "projects\projects.html", context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj #set project for which review submitted
        review.owner = request.user.profile #set owner of review
        review.save()

        projectObj.getVoteCount

        messages.success(request,'Review submitted successfully')
        return redirect('project', pk=projectObj.id)
        
    return render (request, "projects\single-project.html", {'project': projectObj , 'form': form})

#login is required ...if not will route to login page
@login_required(login_url='login')
def createProject(request):

    profile = request.user.profile
    
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid :
            project = form.save(commit=False)
            project.owner=profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
    
    context = {'form':form}
    return render(request, "projects\project_form.html", context)

@login_required(login_url='login')
def updateProject(request, pk):

    profile = request.user.profile # getting Profile object
    project = profile.project_set.get(id=pk) # reverse related object lookup...get specific project related to profile based on id
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',' ').split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid :
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')

    
    context = {'form':form,'project':project}
    return render(request, "projects\project_form.html", context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    context = {'object' : project}
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, "delete_template.html", context)