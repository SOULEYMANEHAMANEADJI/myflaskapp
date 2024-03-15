from datetime import datetime
import random
import string

# Générer le code-barres automatiquement sous forme de chaîne
def generate_barcode():
    # Fonction pour formater l'heure, les minutes et les secondes
    def format_time(time):
        return '{:02d}'.format(time)

    # Générer aléatoirement les trois lettres en majuscules
    def generate_random_letters():
        return ''.join(random.choices(string.ascii_uppercase, k=3))

    # Obtenir les 3 lettres en majuscules aléatoirement
    letters = generate_random_letters()

    # Obtenir la date et l'heure actuelles
    now = datetime.now()

    # Formater les éléments nécessaires
    formatted_time = format_time(now.hour) + format_time(now.minute) + format_time(now.second)
    formatted_day = '{:02d}'.format(now.day)

    # Concaténer tous les éléments pour créer le code-barres sous forme de chaîne
    barcode_data = f"{letters}-{formatted_time}-{formatted_day}"
    return barcode_data

# Appel de la fonction pour générer le code-barres
#generated_barcode = generate_barcode()

# Afficher le code-barres généré
# print("Code-barres généré :", generate_barcode())
