from django_seed import Seed    
from django.contrib.auth.models import User
import random
from django.contrib.auth.hashers import make_password

def run():
    seeder = Seed.seeder()
    
    # Seed pour le modèle Pays
    seeder.add_entity(User, 10, {
        'username': lambda x: seeder.faker.user_name(),
        'first_name': lambda x: seeder.faker.first_name(),
        'last_name': lambda x: seeder.faker.last_name(),
        'email': lambda x: seeder.faker.email(),
        'password': lambda x: make_password("userpassword"),
        'is_staff': 0,
        'is_superuser': 0,
    })


    inserted_pks = seeder.execute()
    print(inserted_pks)
