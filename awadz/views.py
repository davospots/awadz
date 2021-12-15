from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.urls.base import reverse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
import random

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, PostReport, Notification
from users.models import UserReport
from users.models import Profile
from .forms import CommentForm, ReportPostForm, PostForm


@login_required
def home_view(request):
    user = request.user

    if user.is_authenticated:
        
        follows_users = user.profile.follows.all()
        follows_posts = Post.objects.filter(author_id__in=follows_users)
        user_posts = Post.objects.filter(author=user)
        post_list = (follows_posts|user_posts).distinct().order_by('-date_posted')
        page = request.GET.get('page', 1)
        paginator = Paginator(post_list, 4)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
                    'posts': posts,

            }
        return render(request, 'awadz/home.html', context)
    else:
        return redirect('login')

def post_detail_view(request,slug=None):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.author=request.user
            comment.save()
            return redirect('awadz:post-detail', slug=post.slug)
    else:
        form = CommentForm()
        report_form = ReportPostForm()
        comments = Comment.objects.filter(post=post).order_by('-id')
        context = {'post':post,'form':form,'comments':comments,'report_form':report_form}

    return render(request,'awadz/post_detail.html',context)

    
@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author=request.user
            post.save()
            ctx = {'url':post.get_absolute_url()}
            return HttpResponse(json.dumps(ctx), content_type='application/json')

    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request,'awadz/post_form.html',context)


@login_required
def post_update_view(request,pk):
    post1 = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=post1)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            ctx = {'url':post.get_absolute_url()}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        post = get_object_or_404(Post,pk=pk)
        form = PostForm(instance = post)
        context = {
            'form': form,
            'post':post,
        }
        return render(request,'awadz/post_form_update.html',context)

@login_required
def post_delete_view(request, pk=None):
    context = {}
    post = get_object_or_404(Post,pk=pk)
    
    if request.method =="POST":
        if post.author == request.user:
            post.delete()
            return redirect('profile', username=request.user.username)
    context = {"post":post}
    return render(request,'awadz/post_confirm_delete.html',context)



@login_required
def search_view(request):
    
    message = ""
    post_list = Post.objects.all().order_by('-pk');
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    if request.method == 'POST':
        try:
            search_input = request.POST.get('search')
            result_posts = Post.objects.filter(Q(title__icontains=search_input)|Q(content__icontains=search_input))
            users = User.objects.filter(Q(username__iexact=search_input))

            # first condition : post-0 , users-0
            if result_posts.count() == 0 and users.count() == 0:
                message = "No results found for: "+search_input
                context = {'message':message,'posts':posts,'search_input':search_input}
                return render(request,'awadz/search.html',context)

            # second condition : post-yes , users-0
            elif users.count() == 0 and result_posts.count() != 0:
                context = {'result_posts':result_posts,'search_input':search_input,'posts':posts}
                return render(request,'awadz/search.html',context)

            # 3rd condition : post-no , users-yes
            elif result_posts.count() == 0 and users.count() > 0:
                context = {'users':users,'posts':posts,'search_input':search_input}
                return render(request,'awadz/search.html',context)
            
            # 4th condition : post:yes , user: yes
            else:
                context = {'users':users,'result_posts':result_posts,'posts':posts,'search_input':search_input}
                return render(request,'awadz/search.html',context)

        except:
            message = "Unexpected Error Occured!"
            context = {'message':message}
            return render(request,'awadz/search.html',context)
    else:
        flag = True
        context = {'posts':posts,'flag':flag}
        return render(request,'awadz/search.html',context)


@login_required
@require_POST
def like_view(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            like = False
            post_id = '#like'+str(post.id)
        else:
            post.likes.add(user)
            like = True
            post_id = '#like'+str(post.id)
           
    ctx = {'likes_count': post.total_likes,'like':like,'post_id':post_id}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
@require_POST
def post_report_view(request):
    if request.method == 'POST':
        pk = request.POST.get('pk',None)
        reason = request.POST.get('reason')
        post=get_object_or_404(Post,pk=pk)
        user=request.user
        report = PostReport(post=post,reason=reason,user=user)
        report.save()

        return HttpResponse('')

@login_required
@require_POST
def user_report_view(request):
    if request.method == 'POST':
        pk = request.POST.get('pk',None)
        reason = request.POST.get('reason')
        reported_user=get_object_or_404(User,pk=pk)
        report = UserReport(reported_user=reported_user,reason=reason,reporting_user=request.user)
        report.save()

        return HttpResponse('')

@login_required
def notifications_view(request,username=None):
    user = get_object_or_404(User,username=username)
    notifications = Notification.objects.filter(receiver=user).order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(notifications, 6)
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    return render(request,'awadz/notifications.html',{'notifications':notifications})

@login_required
def notifications_update_view(request,username=None):
    user = get_object_or_404(User,username=username)
    if user == request.user:
        notifications = Notification.objects.filter(receiver=user)
        for notification in notifications.all():
            if notification.read == False:
                notification.read = True
                notification.save()
        return HttpResponse('')


@login_required
def notifications_unread_count_view(request,username=None):
    user = get_object_or_404(User,username=username)
    if user == request.user:
        notifications = Notification.objects.filter(receiver=user)
        count = 0
        for notification in notifications.all():
            if notification.read == False:
                count = count+1
        data = {
            'count':count
        }
        return JsonResponse(data)



@login_required(login_url="/accounts/login/")
def rate_project(request, id):
    if request.method == "POST":

        post = Post.objects.get(id=id)
        current_user = request.user

        design_rate=request.POST["design"]
        usability_rate=request.POST["usability"]
        content_rate=request.POST["content"]

        Rating.objects.create(
            post=post,
            user=current_user,
            design_rate=design_rate,
            usability_rate=usability_rate,
            content_rate=content_rate,
            avg_rate=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),
        )

        # get the avarage rate of the project for the three rates
        avg_rating= (int(design_rate)+int(usability_rate)+int(content_rate))/3

        # update the project with the new rate
        post.rate=avg_rating
        post.update_project()

        return render(request, "project.html", {"success": "Project Rated Successfully", "post": post, "rating": Rating.objects.filter(project=project)})
    else:
        post = Post.objects.get(id=id)
        return render(request, "project.html", {"danger": "Project Rating Failed", "post": post})