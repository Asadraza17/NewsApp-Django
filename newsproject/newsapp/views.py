from django.shortcuts import get_object_or_404, redirect, render
import requests
from .models import News
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    r = requests.get('http://api.mediastack.com/v1/news?access_key=e52d724c4fbed0b26d030072076ade63&countries=au')
    res = r.json()
    data = res['data']
    title = []
    description = []
    url = []
    image = []
    for i in range(len(data)):
        title.append(data[i]['title'])
        description.append(data[i]['description'])
        url.append(data[i]['url'])
        image.append(data[i]['image'])
    news = zip(title, description, url, image)
    return render(request, 'newsapp/index.html', {'news': news})    

def login_register(request):
    if request.method == 'POST':
        if 'login_form' in request.POST:
            email = request.POST.get('logemail')
            password = request.POST.get('logpass')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
                return redirect('login_register')
        elif 'register_form' in request.POST:
            name = request.POST.get('logname')
            email = request.POST.get('logemail')
            password = request.POST.get('logpass')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please use a different email.')
                return redirect('login_register')
            else:
                user = User.objects.create_user(email, email, password)
                user.first_name = name
                user.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('login_register')
    return render(request, 'newsapp/login.html')

def login_view(request):
    return render(request, 'newsapp/login.html')

def community(request, news_id=None):
    all_news = News.objects.all().order_by('-created_at')
    context = {'all_news': all_news}
    return render(request, 'newsapp/community.html', context)

@login_required(login_url='login')
def add_news(request):
    return render(request, 'newsapp/addnews.html')

@login_required(login_url='login')
def submit_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        category = request.POST.get('category')
        created_at = request.POST.get('created_at')
        news = News.objects.create(title=title, text=text, category=category, created_at=created_at)
        return redirect('community_with_id', news_id=news.id)

def delete_all_news(request):
    News.delete_all()
    return render(request, 'newsapp/community.html', {})

def logout_view(request):
    logout(request)
    return redirect('index')