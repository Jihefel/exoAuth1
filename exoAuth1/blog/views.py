from django.shortcuts import render, redirect
from .forms import RegistrationForm, ArticleForm
from .models import Article
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, AnonymousUser

def home(request):
    articles = Article.objects.all()
    group_id_member = 1
    group_id_banni = 2
    
    if request.user.id is not None:
        is_member = Group.objects.filter(id=group_id_member, user=request.user).exists()
        is_banned = Group.objects.filter(id=group_id_banni, user=request.user).exists()
        user_articles = Article.objects.filter(user=request.user)

    context = locals()
    return render(request, 'blog/index.html', context)

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
    return render(request, 'blog/inscription.html',{'form':form})

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
                return render(request, 'blog/connexion.html',{'error_message':error_message})
        else:
            return render(request, 'blog/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('home')

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
    return render(request, 'blog/create_article.html', {'form': form})


def delete_article(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('home')