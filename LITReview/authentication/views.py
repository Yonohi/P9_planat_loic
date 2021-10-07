from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from book_review.models import Ticket, Review, UserFollows
from book_review.views import flux
from .forms import LoginForm
from django.conf import settings
from django.db import transaction
from  django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def insc_connect(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
                )
            if user is not None:
                login(request, user)
                return flux(request)
            else:
                message = 'Identifiants incorrects'
    context = {
        'sup_nav':1,
        'form':form,
        'message': message
}
    return render(request, 'authentication/insc_connect.html', context)
    
def inscription(request):
    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_pass')
        try:
            validate_password(password)
            if password == confirm_pass:
                user = User.objects.filter(username=name)
                if not user.exists():
                    user = User.objects.create_user(
                        username=name,
                        password=password
                        )
                    return render(request, 'authentication/insc_connect.html',
                                {'sup_nav':1})
        except ValidationError:
            message = "Le mot de passe n'est pas correct"
    context = {
        'sup_nav':1,
        'message':message
}
    return render(request, 'authentication/inscription.html', context)

def logout_view(request):
    logout(request)
    return insc_connect(request)
