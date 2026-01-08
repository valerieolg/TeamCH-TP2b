import sqlite3
from poste import Poste

class Database:
    def __init__(self, db_path="parc.db"):
        self.db_path = db_path
        self._create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        conn = self.connect() # Ouverture d'une connexion vers la base SQLite
        cursor = conn.cursor() # Le curseur permet d'exécuter des requêtes SQL

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS postes
                       (
                           id        INTEGER PRIMARY KEY AUTOINCREMENT, -- Clé primaire unique pour chaque poste | AUTOINCREMENT garantit un identifiant unique généré automatiquement
                           nom_poste       TEXT NOT NULL,    -- Nom du poste (obligatoire)
                           utilisateur    TEXT NOT NULL,    -- Nom de l'utilisateur (obligatoire)
                           type_poste   TEXT NOT NULL,    -- Type de poste (obligatoire)
                           sys_exploitation     TEXT NOT NULL,     -- Système d'exploitation (obligatoire)
                           adresse_ip     TEXT NOT NULL,     -- Adresse ip (obligatoire)
                           statut     TEXT NOT NULL     -- Statut Actif/En réparation/Hors service (obligatoire)
                       )
                       """)

        conn.commit() # Sauvegarde permanente des changements effectués
        conn.close() # Fermeture explicite de la connexion à la base de données


    STATUTS_AUTORISES = ["Actif", "En réparation", "Hors service"]

    def add_poste(self, poste: Poste):
        if poste.statut not in self.STATUTS_AUTORISES:
            raise ValueError("Statut invalide")

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO postes (nom_poste, utilisateur, type_poste, sys_exploitation, adresse_ip, statut) 
                       -- Indique que l’on veut ajouter un nouvel enregistrement | La table ciblée est postes
                       -- Liste des colonnes dans lesquelles les données seront insérées et l’ordre est important : il doit correspondre aux valeurs fournies ensuite
                       VALUES (?, ?, ?, ?, ?, ?)
                       -- Les ? sont des paramètres SQL (placeholders) | Ils seront remplacés par des valeurs réelles au moment de l’exécution | Chaque ? correspond à une colonne listée au-dessus
                       """,
                       (poste.nom_poste, poste.utilisateur, poste.type_poste, poste.sys_exploitation, poste.adresse_ip, poste.statut))
        conn.commit()
        conn.close()

    def get_all_postes(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT id, nom_poste, utilisateur, type_poste, sys_exploitation, adresse_ip, statut
                       FROM postes
                       """)
        # fetchall() retourne une liste de tuples
        # Chaque tuple représente un poste
        rows = cursor.fetchall()

        conn.close()

        # Les données sont retournées à la couche interface (UI)
        return rows

    def delete_poste(self, poste_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
                       DELETE
                       FROM postes
                       WHERE id = ?
                       """, (poste_id,))
        conn.commit()
        conn.close()

    def update_poste(self, poste_id, poste):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE postes -- Met à jour un contact existant dans la table contacts
            SET nom_poste = ?, utilisateur = ?, type_poste = ?, sys_exploitation = ?, adresse_ip = ?, statut = ? -- Définit les nouvelles valeurs des champs du poste
            WHERE id = ? -- Condition obligatoire pour cibler un seul poste | L'identifiant (id) provient de la clé primaire SQLite
        """, (poste.nom_poste, poste.utilisateur, poste.type_poste, poste.sys_exploitation, poste.adresse_ip, poste.statut, poste_id))
        conn.commit()
        conn.close()

