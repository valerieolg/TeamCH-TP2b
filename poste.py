class Poste:
    def __init__(self, id, nom_poste, utilisateur, type_poste, sys_exploitation, adresse_ip, statut):
        self.id = id
        self.nom_poste = nom_poste
        self.utilisateur = utilisateur
        self.type_poste = type_poste
        self.sys_exploitation = sys_exploitation
        self.adresse_ip = adresse_ip
        self.statut = statut