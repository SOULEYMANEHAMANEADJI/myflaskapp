## Application Blog avec Flask
Ceci est une application web Flask pour un blog simple. Les utilisateurs peuvent s'inscrire, se connecter, afficher des articles, et créer/éditer/supprimer des articles (s'ils sont connectés).
### Fonctionnalités:
Inscription et connexion des utilisateurs
Opérations CRUD d'articles (Créer, Lire, Mettre à jour, Supprimer)
Authentification utilisateur (accès au tableau de bord uniquement pour les utilisateurs connectés)
### Prérequis:
Python 3
Flask
Flask-MySQL
WTForms
Passlib
### Installation:
- Installer les librairies requises :
> pip install Flask Flask-MySQL WTForms passlib
### Configuration:
1. Modifiez le dictionnaire app.config dans le code pour définir les détails de connexion à votre base de données MySQL :
  - MYSQL_HOST
  - MYSQL_USER
  - MYSQL_PASSWORD
  - MYSQL_DB
2. Définissez une clé secrète pour l'application :
  app.secret_key = 'votre_clé_secrète'
### Exécution de l'application:
1. Enregistrez le code sous le nom app.py.
2. Exécutez l'application depuis la ligne de commande :
  Bash
### HAS


