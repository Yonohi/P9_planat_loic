from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from .models import Ticket, Review, UserFollows
from django.conf import settings
from django.db import transaction
from  django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


@login_required   
def flux(request):
    stars = [1,2,3,4,5]
    user = get_user(request)
    user_followeds = [pair.followed_user for pair in UserFollows.objects.filter(user=user)]
    user_posts = []
    user_posts.extend(user_followeds)
    user_posts.append(user)
    list_elemts = []
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    for user_post in user_posts:
        ticket_posts = Ticket.objects.filter(user=user_post)
        review_posts = Review.objects.filter(user=user_post)
        for review in review_posts:
            list_elemts.append(review)
        for ticket in ticket_posts:
            list_elemts.append(ticket)
    context = {
        'list_elemts':sorted(list_elemts, key=lambda x:x.time_created, reverse=True),
        'tickets':tickets,
        'reviews':reviews,
        'user_followeds':user_posts,
        'stars':stars
    }
    return render(request, 'book_review/flux.html', context)

@login_required
def posts(request):
    stars = [1,2,3,4,5]
    list_elemts = []
    actual_user = get_user(request)
    tickets = Ticket.objects.filter(user=actual_user)
    reviews = Review.objects.filter(user=actual_user)
    for review in reviews:
        list_elemts.append(review)
    for ticket in tickets:
        list_elemts.append(ticket)
    context = {
        'list_elemts':sorted(list_elemts, key=lambda x:x.time_created, reverse=True),
        'tickets':tickets,
        'reviews':reviews,
        'stars':stars
    }
    return render(request, 'book_review/posts.html', context)

@login_required
def abonnements(request):
    user = get_user(request)
    if request.method == "POST":
        if 'sub' in request.POST:
            name = request.POST.get('name')
            followed_user = User.objects.get(username=name)
            if name in [user.username for user in User.objects.all()] \
                    and name != user.username \
                    and not name in [pair.followed_user.username for pair in UserFollows.objects.filter(user=user)]:
                pair = UserFollows(
                    user=user,
                    followed_user=followed_user
                )
                pair.save()
        elif 'unsub' in request.POST:
            unsub_name = request.POST.get('unsub')
            unsub_user = User.objects.get(username=unsub_name)
            unsub_pair = UserFollows.objects.get(user=user, followed_user=unsub_user)
            unsub_pair.delete()
    followed_users = UserFollows.objects.filter(user=user)
    followed_bys = UserFollows.objects.filter(followed_user=user)
    context = {
        "followed_users":followed_users,
        "followed_bys": followed_bys,
        "user":user
}

    return render(request, 'book_review/abonnements.html', context)


@login_required
def crea_ticket(request, ticket_id=""):
    context = {}
    if ticket_id:
        ticket = Ticket.objects.get(id=ticket_id)
        context["ticket"]=ticket
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        user = get_user(request)
        image = request.FILES.get("image")
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.title = title
            ticket.description = description
            ticket.image = image
            ticket.save()
        else:
            ticket = Ticket(
                title=title,
                description=description,
                user=user,
                image=image
            )
            ticket.save()
        return flux(request)
    return render(request, 'book_review/crea_ticket.html', context)

@login_required   
def crea_review(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        user = get_user(request)
        image = request.FILES.get('image')
        ticket = Ticket(
            title=title,
            description=description,
            user=user,
            image=image
        )
        ticket.save()
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        review = Review(
            rating=rating,
            headline=headline,
            body=body,
            user=user,
            ticket=ticket
        )
        review.save()
        return flux(request)
    context = {
}
    return render(request, 'book_review/crea_review.html', context)

@login_required   
def reply_ticket(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id)[0]
    context = {
    'ticket':ticket
}
    if request.method == "POST":
        user = get_user(request)
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        review = Review(
            rating=rating,
            headline=headline,
            body=body,
            user=user,
            ticket=ticket
        )
        review.save()
        return flux(request)

    return render(request, 'book_review/reply_ticket.html', context)
