from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.password_validation import validate_password
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
                return redirect("book_review:flux")
            else:
                message = 'Identifiants incorrects'
    context = {
        'sup_nav': 1,
        'form': form,
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
            test_user = User.objects.filter(username=name)
            if test_user:
                raise ValueError
            validate_password(password)
            if password == confirm_pass:
                user = User.objects.filter(username=name)
                if not user.exists():
                    user = User.objects.create_user(
                        username=name,
                        password=password
                        )
                    login(request, user)
                    return redirect("book_review:flux")
        except ValueError:
            message = "Le nom d'utilisateur existe déjà"
        except ValidationError:
            message = "Le mot de passe n'est pas correct"
    context = {
        'sup_nav': 1,
        'message': message
    }
    return render(request, 'authentication/inscription.html', context)


def logout_view(request):
    logout(request)
    return insc_connect(request)
