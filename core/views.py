from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Profile
from .forms import TweetForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate


def home_page(req):
    return render(req, 'core/base.html')


def tweet_list(req):
    query = req.GET.get('q', '').strip()
    tweets = Tweet.objects.all().order_by('-created_at')
    if query:
        tweets = tweets.filter(user__username__icontains = query)
    return render(req, 'core/tweet_list.html', {'tweets': tweets, 'isTweetList': True})


def my_tweets(req):
    tweets = Tweet.objects.filter(user = req.user).order_by('-created_at')
    return render(req, 'core/my_tweets.html', {'my_tweets': tweets})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Tweet.objects.filter(user = user).order_by('-created_at')
    is_following = request.user.profile.is_following(profile)
    return render(request, 'core/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile', username=request.user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'core/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def display_profiles(req):
    profiles = Profile.objects.exclude(user=req.user)
    return render(req, 'core/users.html', {'profiles': profiles})


def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    request.user.profile.follow(user_to_follow.profile)
    return redirect('profile', username=username)

def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.profile.unfollow(user_to_unfollow.profile)
    return redirect('profile', username=username)


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    followers = profile.followers.all()  
    return render(request, 'core/followers_list.html', {
        'profile_user': user,
        'followers': followers
    })

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    following = profile.following.all()  
    return render(request, 'core/following_list.html', {
        'profile_user': user,
        'following': following
    })


@login_required
def tweet_create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, "Tweet created successfully!")
            return redirect('my_tweets')
        pass
    else:
        form = TweetForm()
    return render(req, 'core/tweet_form.html', {'form': form})


@login_required
def tweet_edit(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = req.user)
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, "Tweet updated successfully!")
            return redirect('my_tweets')

    else:
        form = TweetForm(instance=tweet)
    return render(req, 'core/tweet_form.html', {'form': form})


@login_required
def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    
    tweet.delete()
    messages.success(req, "Tweet deleted successfully!")
    return redirect('my_tweets')


def register(req):
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            login(req, user)
            req.session.set_expiry(0)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(req, 'registration/register.html', {'form': form})


def login_user(req):
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=uname, password=password)
            if user is not None:
                login(req, user)
                req.session.set_expiry(0)
                return redirect('tweet_list')
            else:
                messages.warning(req, 'Invalid user')
                return redirect('tweet_list')
        else:
            messages.warning(req, 'Invalid user')
            return redirect('tweet_list')
    else:
        form = AuthenticationForm()
        return render(req, 'registration/login.html', {'form': form})


def logout_user(req):
    logout(req)
    return render(req, 'registration/logged_out.html')