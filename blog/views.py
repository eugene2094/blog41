from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View

from .forms import PostForm, UserRegistrationForm, ProfileUpdateForm
from .models import Post, Category, Profile
from django.db.models import Q


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2
    first_half = all[:half]
    second_half = all[half:]
    return {'cats1': first_half, 'cats2': second_half}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    # posts = Post.objects.filter(content__icontains="lorem")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def category(request, c=None):
    cObj = get_object_or_404(Category, name=c)
    posts = Post.objects.filter(category=cObj).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def post(request, name=None):
    post = get_object_or_404(Post, title=name)
    context = {'post': post}
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def contact(request):
    context = {}
    context.update(get_categories())
    return render(request, "blog/contact.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return index(request)
    form = PostForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, "blog/create.html", context)


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


@login_required
def profile(request):
    # profile_data = Profile.objects.get(user=request.user)
    # context = {'profile_data': profile_data, 'user': request.user}
    # context.update(get_categories())
    return render(request, "blog/profile.html")


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/profileUpdate.html', context)

from django.contrib.auth.hashers import make_password

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful.')
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/registration.html', context)

