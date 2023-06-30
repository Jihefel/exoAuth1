from django.shortcuts import render, redirect
from .forms import RegistrationForm, ArticleForm, CustomPasswordChangeForm
from .models import Article
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q


def send_confirmation(user):

    send_mail(
    f"{user.username}, your password has been changed",
    "",
    "from@example.com",
    ["to@example.com"],
    html_message=render_to_string('mails/confirm_password.html', {'user': user}),
    )


def home(request):
    articles = Article.objects.all()
    users = User.objects.all()
    group_id_member = 1
    group_id_banni = 2
    
    if request.user.id is not None:
        is_member = Group.objects.filter(id=group_id_member, user=request.user).exists()
        is_banned = Group.objects.filter(id=group_id_banni, user=request.user).exists()
        user_articles = Article.objects.filter(user=request.user)

    context = locals()
    return render(request, 'blog/pages/index.html', context)

def search_user(request):
    if request.method == 'POST':
        search_string = request.POST.get('search')  # Récupère le contenu de l'input avec le name "search"
        users = User.objects.filter(
            Q(username__icontains=search_string) | 
            Q(username__iexact=search_string)
        )
        context = locals()
        return render(request, 'blog/pages/index.html', context)
    else:
        return redirect("home")


def inscription(request):
    articles = Article.objects.all()
    # Obtenez tous les groupes
    groups = Group.objects.all()

    # Obtenez un groupe spécifique par ID
    group = Group.objects.get(id=1)

    # Obtenez tous les utilisateurs "Membre"
    member = group.user_set.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'blog/pages/inscription.html',{'form':form})

def connexion(request):
    articles = Article.objects.all()
    # Obtenez tous les groupes
    groups = Group.objects.all()

    # Obtenez un groupe spécifique par ID
    group = Group.objects.get(id=1)

    # Obtenez tous les utilisateurs "Membre"
    member = group.user_set.all()


    if not AnonymousUser:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Nom d'utilisateur ou mot de passe incorrect."
                return render(request, 'blog/pages/connexion.html',{'error_message':error_message})
        else:
            return render(request, 'blog/pages/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('home')

@login_required(login_url = 'connexion')
def profile(request):
    # Obtenez tous les groupes
    groups = Group.objects.all()

    # Obtenez un groupe spécifique par ID
    group = Group.objects.get(id=1)

    # Obtenez tous les utilisateurs "Membre"
    member = group.user_set.all()


    context = locals()  
    return render(request, 'blog/pages/profil.html', context)

@login_required(login_url = 'connexion')
def change_password(request):
    # Obtenez tous les groupes
    groups = Group.objects.all()

    # Obtenez un groupe spécifique par ID
    group = Group.objects.get(id=1)

    # Obtenez tous les utilisateurs "Membre"
    member = group.user_set.all()

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=request.user)  # Met à jour la session de l'utilisateur avec le nouveau mot de passe
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            send_confirmation(request.user)
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = locals()  
    return render(request, 'blog/pages/change_password.html', context)


@login_required(login_url = 'connexion')
def create_article(request):
    articles = Article.objects.all()
    # Obtenez tous les groupes
    groups = Group.objects.all()

    # Obtenez un groupe spécifique par ID
    group = Group.objects.get(id=1)

    # Obtenez tous les utilisateurs "Membre"
    member = group.user_set.all()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'blog/pages/create_article.html', {'form': form})


def delete_article(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('home')