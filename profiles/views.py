from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from profiles.forms import PostingForm, SearchForm, RegisterForm
from profiles.models import Posting, Following


def home(request):
    search_form = SearchForm()
    context = {'search_form': search_form}
    return render(request, 'site/home.html', context)


def profile(request):
    search_form = SearchForm()
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            posting = Posting()
            posting.content = content
            posting.author = request.user
            posting.save()
            return HttpResponseRedirect('/profile')
    else:
        form = PostingForm()
    postings = Posting.objects.order_by('-posted_on')
    current_uid = request.user.id
    follows = Following.objects.filter(user_id=current_uid)
    followed_users = []
    for record in follows:
        followed_users.append(record.follows)
    context = {'postings': postings, 'form': form, 'search_form': search_form, 'follows': followed_users}
    return render(request, 'site/profile.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['term']
            postings = Posting.objects.filter(content__contains=term)
            form = SearchForm()
            context = {'postings': postings, 'search_form': form, 'term': term}
            return render(request, 'site/search.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login')

    register_form = RegisterForm()
    context = {'register_form': register_form}
    return render(request, 'registration/register.html', context)


def like_post(request, pid):
    uid = request.user.id
    post = Posting.objects.get(pk=pid)
    if post.likes.filter(id=uid).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('/profile')


def follow(request, uid):
    current_uid = request.user.id
    following = Following()
    following.user_id = current_uid
    following.follows_id = uid
    following.save()
    return redirect('/profile')


def following(request):
    current_uid = request.user.id
    follows = Following.objects.filter(user_id=current_uid)
    context = {'follows': follows}
    return render(request, 'site/following.html', context)
