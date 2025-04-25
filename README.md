# 🐰 Élevage de Lapins – Jeu de Gestion Stratégique

Bienvenue dans **Élevage de Lapins**, un jeu de stratégie au tour par tour développé dans le cadre d’un projet de cours. Le joueur incarne un gestionnaire d’élevage devant optimiser l’utilisation de ses ressources pour faire prospérer son élevage de lapins.


---

## 🎯 Objectif du Jeu

Le but du jeu est de faire croître un élevage de lapins en gérant intelligemment les ressources suivantes :

- 🐇 Lapins (mâles, femelles, reproduction, vente)
- 🌾 Nourriture
- 🏠 Cages
- 💰 Argent en caisse

Le joueur doit prendre des décisions stratégiques à chaque tour pour vendre, acheter, nourrir, et maintenir un élevage en bonne santé.

---

## 🧩 Mécanismes de Jeu

### Démarrage

- Une **page d’initialisation** permet de configurer les ressources de départ.
- Le joueur choisit :
  - Le nombre initial de lapins
  - La quantité de nourriture
  - Le nombre de cages
  - L’argent disponible

### Tour par tour

Chaque tour représente **un mois**. Le joueur peut :

- Vendre des lapins
- Acheter de la nourriture ou des cages
- Terminer le tour pour voir les événements simulés

### Règles de simulation

- 🐇 **Reproduction** :
  - Femelles matures à 6 mois
  - Gestation : 1 mois
  - Portées : 1 à 4 lapereaux
  - Reproductives jusqu’à 4 ans

- 🍽️ **Alimentation** :
  - Adulte : 250 g/jour
  - Lapereau :
    - 0-1 mois : lait maternel
    - 1-2 mois : 100 g/jour
    - 2+ mois : 250 g/jour
  - Si manque de nourriture → mort

- 🏠 **Cages** :
  - Capacité normale : 6 lapins par cage
  - 10+ lapins/cage : risque accru de maladie
  - Lapereaux <1 mois ne comptent pas dans la surpopulation

---

## 🧪 Fonctionnalités à Tester

- ✅ Formulaire d’initialisation d’une partie
- ✅ Liste des élevages en cours avec navigation vers les détails
- ✅ Page de détails d’un élevage avec état des ressources et actions disponibles
- ✅ Système de passage au tour suivant avec mise à jour selon les règles ci-dessus

---
