import re
import ipaddress

# Classe responsable de la validation des entrées de l'utilisateur
class Catch:

    @staticmethod
    def input_nom_poste(value: str):
        if not value.strip():
            return False, "nom du poste", "Ce champ ne peut pas être vide."
        regex = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9_\- ]+$"
        if not re.fullmatch(regex, value):
            return False, "nom du poste", "Le nom contient des caractères invalides."
        return True, None, ""

    @staticmethod
    def input_utilisateur(value: str):
        if not value.strip(): # Vérifie d’abord si le champ est vide
            return False, "utilisateur", "Ce champ ne peut pas être vide."

        regex = r"^[A-Za-z0-9._\-]+$" # Accepte les lettres, tirets, barres de soulignement, chiffres
        if not re.fullmatch(regex, value):
            return False, "utilisateur", "L'utilisateur contient des caractères invalides."

        return True, None, ""

    @staticmethod
    def input_type_poste(value: str):
        if not value.strip(): # Vérifie d’abord si le champ est vide
            return False, "type du poste", "Le type de poste est obligatoire."

        regex = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9 \-]+$" # Accepte les lettres, accents, espaces, tirets, apostrophes, chiffres
        if not re.fullmatch(regex, value):
            return False, "type du poste", "Le type de poste contient des caractères invalides."

        return True, None, ""

    @staticmethod
    def input_adresse_ip(value: str):
        try:
            ipaddress.IPv4Address(value)
            return True, None, ""
        except ValueError:
            return False, "adresse ip", "Adresse IP invalide."

    @staticmethod
    def input_statut(value: str):
        STATUTS_AUTORISES = {"Actif", "En réparation", "Hors service"}
        if value not in STATUTS_AUTORISES:
            return False, "statut", "Statut invalide."
        return True, None, ""

    @staticmethod
    def input_sys_exploitation(value: str):
        if not value.strip():
            return False, "système d'exploitation", "Le système d'exploitation est obligatoire."
        regex = r"^[A-Za-z0-9.\-+ ]+$"
        if not re.fullmatch(regex, value):
            return False, "système d'exploitation", "Le système d'exploitation contient des caractères invalides."
        return True, None, ""

    # Méthode qui renvoit exactement quel champ pose problème
    @staticmethod
    def validate_poste(nom_poste, utilisateur, type_poste, adresse_ip, statut, sys_exploitation):
        validations = [
            Catch.input_nom_poste(nom_poste),
            Catch.input_utilisateur(utilisateur),
            Catch.input_type_poste(type_poste),
            Catch.input_adresse_ip(adresse_ip),
            Catch.input_statut(statut),
            Catch.input_sys_exploitation(sys_exploitation),
        ]

        for is_valid, field, message in validations:
            if not is_valid:
                return False, field, message
                # False → contact invalide
                # field → nom du champ à colorer
                # message → message d’erreur à afficher

        return True, None, ""
