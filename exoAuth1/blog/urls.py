from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('create_article/', views.create_article, name='create_article'),

    path('delete_article/<int:id>', views.delete_article, name='delete_article'),
]
