from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='basic')
    Group.objects.get_or_create(name='premium')

@receiver(post_save, sender=User)
def add_user_to_basic_group(sender, instance, created, **kwargs):
    if created:  # Vérifie si c'est un nouvel utilisateur
        basic_group = Group.objects.get(name='basic')
        instance.groups.add(basic_group)  # Ajoute l'utilisateur au groupe "basic"
