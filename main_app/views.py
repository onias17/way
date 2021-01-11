from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ProfileCreationForm, PostCreationForm, CityCreationForm, CommentCreationForm
from .models import Profile, Post, City, Comment
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import datetime as dt
import humanize
from django.utils.text import slugify

CITIES = [ 'Irvine' , 'New York' ]

# Create your views here.

def home(request):
    city = City.objects.latest('id')
    post = Post.objects.latest('id')
    profile = Profile.objects.latest('id')

    post.content = post.content[:100]

    context = {
        'city': city,
        'post': post,
        'profile': profile
    }
    return render(request, 'home.html', context)

## PROFILES VIEWS

def profiles_index(request):
    profile = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(profile=profile)
    

    for post in posts:
        post.content = post.content[:100]
        context = {'profile': profile, 'posts' : posts}
    return render(request, 'profiles/index.html', context)

@login_required
def new_profile(request):
    if request.method == "POST":
        profile_form = ProfileCreationForm(request.POST, request.FILES)
        if profile_form.is_valid():
            new_profile = profile_form.save(commit=False)
            new_profile.user = request.user
            new_profile.slug = slugify(new_profile.user.username)
            new_profile.save()

            # email = request.POST.get('email', '')
            # data = """ 
            # Hello There!
            # Welcome to Wayfarer, the site with all of the information you need for your future travels. 
            # We hope you enjoy our site.
            # -Wayfarer
            # """
            # send_mail('Welcome!', data, "Wayfarer",
            # [email], fail_silently=False)
            return redirect('detail', new_profile.slug)
    else:
        profile_form = ProfileCreationForm()
        context = {'profile_form' : profile_form}
        return render(request, 'profiles/new.html', context)

def profiles_detail(request, slug):
    profile = Profile.objects.get(slug=slug)
    posts = Post.objects.filter(profile=profile)
    for post in posts:
        post.content = post.content[:100]
    context = {'profile' : profile, "posts" :posts}

    return render(request, 'profiles/detail.html', context )

@login_required
def profiles_edit(request, slug):
    profile = Profile.objects.get(slug=slug)

    if request.method == "POST":
        profile_form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            updated_profile = profile_form.save()
            return redirect('detail', slug)
    else:
        profile_form  = ProfileCreationForm(instance=profile)
        context = {'profileform': profile_form, 'profile' : profile}
        return render(request, 'profiles/edit.html', context)

def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('new_profile')
        else:
            error_message = "Invalid sign up - try again"
            form = UserCreationForm()
            context = {'form': form, 'error_message': error_message}
            return render(request, 'registration/signup.html', context)

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def add_post(request, slug):
    profile = Profile.objects.get(slug=slug)
    if request.method == "POST":
        cityname = request.POST.get('city')
        form = PostCreationForm(request.POST, request.FILES)
        for city in City.objects.all():
            if city.name == cityname:
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.profile = profile
                    new_form.city = city
                    new_form.save()
                    return redirect('profiles_index')
        else: 
            createdcity = City.objects.create(name=cityname, slug=slugify(cityname))
            new_form = form.save(commit=False)
            new_form.profile = profile
            new_form.city = createdcity
            new_form.save()
        return redirect('profiles_index')
    ##GET REQUEST    
    else:
        cities = City.objects.all()
        form = PostCreationForm()
        return render(request, 'posts/new.html', {'form': form, 'profile' : profile, 'citylist' : cities})


def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.all
    comments_count = Comment.objects.all()
    
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentCreationForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentCreationForm()
    context = {'post': post, "comment_form" : comment_form, 'comments' : comments, 'new_comment' : new_comment, "comments_count": comments_count}
    return render(request, 'posts/detail.html', context)

@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        postform = PostCreationForm(request.POST, request.FILES, instance=post,)
        if postform.is_valid():
            updated_post = postform.save()
            return redirect('postdetail', updated_post.id)
    else:
        postform = PostCreationForm(instance=post)
        context = {'postform': postform, 'post' : post}
        return render(request, 'posts/edit.html', context )

@login_required
def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()

    return redirect("profiles_index")

def city_index(request):
    cities = City.objects.all()
    return render(request, 'cities/index.html', {"cities" : cities})

@login_required
def add_city(request):
    if request.method == "POST":
        form = CityCreationForm(request.POST)
        if form.is_valid():
            new_city = form.save()
            new_city.slug = slugify(new_city.name)
            new_city.save()
            return redirect('citydetail', new_city.slug)
        
    else :
        form = CityCreationForm()
        return render(request, 'cities/new.html', {'form': form})

def city_detail(request, slug):
    city = City.objects.get(slug=slug)
    posts = Post.objects.filter(city=city)
    for post in posts:
        post.content = post.content[:100]

    for post in posts:
        post.date = humanize.naturalday(post.date).title()
    context = {'city': city, 'posts' : posts}
    return render(request, 'cities/detail.html', context)

def success(request):
    # email = request.POST.get('email', '')
    # data = """ 
    # Hi welcome
    # to
    # Wayfarer
    # """
    # send_mail('Welcome!', data, "Wayfarer"
    # [email], fail_silently=False)
    return render(request, '')


##TESTING OUT ADDING A CITY FROM CITY PAGE
def add_citypost(request, city_id):
    if request.method == "POST":
        city = City.objects.get(id=city_id)
        profile = Profile.objects.get(id=request.user.profile.id)
        form = PostCreationForm(request.POST, request.FILES)
        

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.profile = profile
            new_form.city = city
            new_form.save()

        return redirect('postdetail', new_form.id)
    else:
        city = City.objects.get(id=city_id)
        profile = Profile.objects.get(id=request.user.profile.id)
        form = PostCreationForm()
        return render(request, 'posts/new2.html', {'form':form, 'profile' : profile, "city" : city})

def add_comment(request, post_id):
    form = CommentCreationForm(request.POST)
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(id = request.user.profile.id)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.post = post
        new_form.profile = profile
        new_form.save()

    return redirect('postdetail', post_id)

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    comment.delete()
    return redirect('postdetail', post.id)