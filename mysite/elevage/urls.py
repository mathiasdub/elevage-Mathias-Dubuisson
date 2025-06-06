from django.urls import path,include
from . import views

from django.contrib.auth import views as auth_views




app_name = "elevage"
urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("nouveau/", views.nouveau, name="nouveau"),
    path("liste/", views.liste, name="liste"),
    path("elevage/<int:elevage_id>/", views.detail, name="detail"),
    path("regles", views.liste_regle, name="regles"),
    path("elevage/<int:elevage_id>/supprimer", views.supprimer_elevage, name="supprimer"),
    path("datas/<int:elevage_id>/", views.get_datas, name="get_datas"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('paiement/', views.paiement, name='paiement'),
    path("elevage/<int:elevage_id>/restaurer/<int:tour>/", views.restaurer_tour, name="restaurer_tour")
]