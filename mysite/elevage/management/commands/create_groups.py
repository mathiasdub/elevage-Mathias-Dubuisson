from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Crée les groupes basic et premium et affecte les utilisateurs au groupe basic'

    def handle(self, *args, **kwargs):
        # Créer ou récupérer les groupes
        basic_group, created = Group.objects.get_or_create(name='basic')
        premium_group, created = Group.objects.get_or_create(name='premium')

        # Affecter tous les utilisateurs au groupe "basic" par défaut
        users = User.objects.all()
        for user in users:
            user.groups.add(basic_group)  # Ajoute chaque utilisateur au groupe "basic"
        
        self.stdout.write(self.style.SUCCESS('Groupes créés et utilisateurs ajoutés au groupe "basic" par défaut!'))
