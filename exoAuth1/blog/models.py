from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Groupe Member par défaut
@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Member')  # Remplacez 'NomDuGroupe' par le nom de votre groupe par défaut
        instance.groups.add(group)
post_save.connect(assign_default_group, sender=User)


