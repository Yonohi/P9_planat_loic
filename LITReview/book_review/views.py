from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from .models import Ticket, Review, UserFollows
import os


STARS = [1, 2, 3, 4, 5]

@login_required   
def flux(request):
    # On sélectionne l'utilisateur et les personnes suivies
    user = get_user(request)
    user_followeds = [pair.followed_user for pair in UserFollows.objects.filter(user=user)]
    user_posts = []
    user_posts.extend(user_followeds)
    user_posts.append(user)
    list_elemts = []
    # On recherche les tickets et reviews souhaitées
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    for user_post in user_posts:
        ticket_posts = Ticket.objects.filter(user=user_post)
        review_posts = Review.objects.filter(user=user_post)
        for review in review_posts:
            list_elemts.append(review)
        for ticket in ticket_posts:
            list_elemts.append(ticket)
    # On recherche les reviews des non abonnés
    user_tickets = Ticket.objects.filter(user=user)
    for ticket in user_tickets:
        review_user_tickets = Review.objects.filter(ticket=ticket)
        for review in review_user_tickets:
            if review not in list_elemts:
                list_elemts.append(review)
    # On tri par ordre chronologique
    sorted_list = sorted(list_elemts,
                         key=lambda x: x.time_created,
                         reverse=True)
    # On recherche les reviews de l'utilisateur
    user_review = Review.objects.filter(user=user)
    # On créé une liste de tickets déjà critiqué par l'utilisateur
    tickets_stop_btn = [review.ticket for review in user_review]
    context = {
        'list_elemts': sorted_list,
        'tickets_stop_btn': tickets_stop_btn,
        'tickets': tickets,
        'reviews': reviews,
        'user_followeds': user_posts,
        'stars': STARS
    }
    return render(request, 'book_review/flux.html', context)


@login_required
def posts(request):
    list_elemts = []
    actual_user = get_user(request)
    tickets = Ticket.objects.filter(user=actual_user)
    reviews = Review.objects.filter(user=actual_user)
    for review in reviews:
        list_elemts.append(review)
    for ticket in tickets:
        list_elemts.append(ticket)
    # Cas où l'utilisateur appuis sur le bouton supprimer pour un ticket
    if 'ticket_delete' in request.POST:
        id_to_delete = request.POST.get('ticket_delete')
        ticket_to_delete = Ticket.objects.get(id=id_to_delete)
        if os.path.exists(ticket_to_delete.image.path):
            os.remove(ticket_to_delete.image.path)
        ticket_to_delete.delete()
        return redirect('book_review:posts')
    # Cas où l'utilisateur appuis sur le bouton supprimer pour une review
    if 'review_delete' in request.POST:
        id_to_delete = request.POST.get('review_delete')
        review_to_delete = Review.objects.get(id=id_to_delete)
        review_to_delete.delete()
        return redirect('book_review:posts')
    context = {
        'list_elemts': sorted(list_elemts,
                              key=lambda x: x.time_created,
                              reverse=True),
        'tickets': tickets,
        'reviews': reviews,
        'stars': STARS
    }
    return render(request, 'book_review/posts.html', context)


@login_required
def abonnements(request):
    user = get_user(request)
    message = ''
    if request.method == "POST":
        # Cas où l'utilisateur souhaite suivre quelqu'un
        if 'sub' in request.POST:
            name = request.POST.get('name')
            if name in [user.username for user in User.objects.all()] \
                    and name != user.username \
                    and name not in [pair.followed_user.username for pair in UserFollows.objects.filter(user=user)]:
                pair = UserFollows(
                    user=user,
                    followed_user=User.objects.get(username=name)
                )
                pair.full_clean()
                pair.save()
            else:
                message = 'Il y a un problème avec le nom rentré, veuillez recommencer.'
        # Cas où l'utilisateur souhaite arrêter de suivre une personne
        elif 'unsub' in request.POST:
            unsub_name = request.POST.get('unsub')
            unsub_user = User.objects.get(username=unsub_name)
            unsub_pair = UserFollows.objects.get(user=user,
                                                 followed_user=unsub_user)
            unsub_pair.delete()
    followed_users = UserFollows.objects.filter(user=user)
    followed_bys = UserFollows.objects.filter(followed_user=user)
    context = {
        "followed_users": followed_users,
        "followed_bys": followed_bys,
        "user": user,
        'message': message
    }

    return render(request, 'book_review/abonnements.html', context)


@login_required
def crea_ticket(request, ticket_id=""):
    context = {}
    if ticket_id:
        ticket = Ticket.objects.get(id=ticket_id)
        context["ticket"] = ticket
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        user = get_user(request)
        image = request.FILES.get("image")
        # Cas où l'on va modifier un ticket existant
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.title = title
            ticket.description = description
            if image:
                if os.path.exists(ticket.image.path):
                    os.remove(ticket.image.path)
                ticket.image = image
            ticket.full_clean()
            ticket.save()
        # Cas où l'on créé un nouveau ticket
        else:
            ticket = Ticket(
                title=title,
                description=description,
                user=user,
                image=image
            )
            ticket.full_clean()
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
        ticket.full_clean()
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
        review.full_clean()
        review.save()
        return flux(request)
    context = {
    }
    return render(request, 'book_review/crea_review.html', context)


@login_required   
def reply_ticket(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id)[0]
    context = {
        'ticket': ticket
    }
    user = get_user(request)
    test_review = Review.objects.filter(ticket=ticket, user=user)
    if test_review:
        context['actual_review'] = test_review[0]
    if request.method == "POST":
        user = get_user(request)
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        # Cas de modification de review
        if test_review:
            test_review[0].rating = rating
            test_review[0].headline = headline
            test_review[0].body = body
            test_review[0].full_clean()
            test_review[0].save()
        # Cas de création de review
        else:
            review = Review(
                rating=rating,
                headline=headline,
                body=body,
                user=user,
                ticket=ticket
            )
            review.full_clean()
            review.save()
        return flux(request)

    return render(request, 'book_review/reply_ticket.html', context)
