from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from db.database import Database
from poste import Poste
from catch.input_errors import Catch

class AddPosteWindow(QWidget):
    def __init__(self, poste_data=None, on_save_callback=None):
        # Appel du constructeur de la classe parente QWidget
        super().__init__()

        # Données du poste à modifier (None si on est en mode ajout)
        # Contient : (id, nom_poste, utilisateur, type_poste, sys_exploitation, adresse_ip, statut)
        self.poste_data = poste_data

        # Fonction de rappel (callback) appelée après un enregistrement réussi
        # Permet de rafraîchir la table dans la fenêtre principale
        self.on_save_callback = on_save_callback

        # Identifiant SQLite du poste
        # Utilisé uniquement en mode modification
        self.poste_id = None

        self.setWindowTitle("Modifier un poste" if poste_data else "Ajouter un poste")
        self.setMinimumSize(420, 280)

        #Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        #Titre
        title = QLabel(self.windowTitle())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        #Formulaire
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.input_nom_poste = QLineEdit()
        self.input_utilisateur = QLineEdit()
        self.input_type_poste = QLineEdit()
        self.input_adresse_ip = QLineEdit()
        self.input_statut = QComboBox()
        self.input_sys_exploitation = QLineEdit()

        self.input_nom_poste.setPlaceholderText("Nom du poste")
        self.input_utilisateur.setPlaceholderText("Utilisateur")
        self.input_type_poste.setPlaceholderText("Type de poste")
        self.input_adresse_ip.setPlaceholderText("Adresse IP")
        self.input_statut.addItems(["Actif", "En réparation", "Hors service"])
        self.input_sys_exploitation.setPlaceholderText("Système d'exploitation")

        form_layout.addRow("Nom du poste :", self.input_nom_poste)
        form_layout.addRow("Utilisateur :", self.input_utilisateur)
        form_layout.addRow("Type de poste :", self.input_type_poste)
        form_layout.addRow("Adresse IP :", self.input_adresse_ip)
        form_layout.addRow("Statut :", self.input_statut)
        form_layout.addRow("Système d'exploitation :", self.input_sys_exploitation)

        # Si des données de poste sont fournies, la fenêtre est en mode édition
        if poste_data:
            # Extraction de l'identifiant unique et des informations du poste
            # Ces données proviennent de la sélection dans la QTableView
            self.poste_id, nom_poste, utilisateur, type_poste, adresse_ip, statut, sys_exploitation = poste_data

            # Initialisation des champs du formulaire avec les données existantes
            # afin de permettre à l'utilisateur de modifier le poste
            self.input_nom_poste.setText(nom_poste)
            self.input_utilisateur.setText(utilisateur)
            self.input_type_poste.setText(type_poste)
            self.input_adresse_ip.setText(adresse_ip)
            self.input_statut.findText(statut)
            index = self.input_statut.findText(statut)
            self.input_sys_exploitation.setText(sys_exploitation)


            if index >= 0:
                self.input_statut.setCurrentIndex(index)
            self.input_sys_exploitation.setText(sys_exploitation)

        #Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.setMinimumWidth(110)
        btn_cancel.setMinimumWidth(110)

        btn_save.clicked.connect(self.save_poste)
        btn_cancel.clicked.connect(self.close)

        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)

        #Assemblage
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    # Sauvegarde (AJOUT ou MODIFICATION)
    def save_poste(self):
        # Récupération des valeurs
        nom = self.input_nom_poste.text()
        utilisateur = self.input_utilisateur.text()
        type_poste = self.input_type_poste.text()
        ip = self.input_adresse_ip.text()
        statut = self.input_statut.currentText()
        systeme = self.input_sys_exploitation.text()

        field_map = {
            "nom du poste": [self.input_nom_poste],
            "utilisateur": [self.input_utilisateur],
            "type de poste": [self.input_type_poste],
            "adresse ip": [self.input_adresse_ip],
            "statut": [self.input_statut],
            "système d'exploitation": [self.input_sys_exploitation]
        }

        # Réinitialise le style de tous les champs du formulaire
        # Cela permet de supprimer les bordures rouges ajoutées
        # lors d'une validation précédente
        for widgets in field_map.values():
            for widget in widgets:
                widget.setStyleSheet("")

        #  Validation des input par catch
        is_valid, field, message = Catch.validate_poste(
             nom, utilisateur, type_poste, ip, statut, systeme
         )

        if not is_valid:
            widgets = field_map.get(field)
            if widgets:
                for widget in widgets:
                    widget.setStyleSheet("border: 2px solid red;")
                    widget.setFocus()

            QMessageBox.warning(self, "Erreur de validation", message)
            return

        # Création de l'objet Poste
        poste = Poste(nom_poste=nom, utilisateur=utilisateur, type_poste=type_poste, adresse_ip=ip, statut=statut, sys_exploitation=systeme)
        db = Database()

        # Si des données de poste existent, cela signifie que l'utilisateur modifie un poste déjà présent dans la base de données
        if self.poste_data:
            # Exécution d'une requête UPDATE en utilisant l'identifiant SQLite
            db.update_poste(self.poste_id, poste)
            message = "Poste modifié avec succès."
        else:
            # Aucun poste existant : création d'un nouveau poste
            # Exécution d'une requête INSERT
            db.add_poste(poste)
            message = "Poste ajouté avec succès."

        QMessageBox.information(self, "Succès", message)

        # Vérifie si une fonction de rappel (callback) a été fournie
        # Si oui, elle est appelée après l'enregistrement réussi
        # afin de rafraîchir la liste des postes dans la fenêtre principale
        if self.on_save_callback:
            self.on_save_callback()

        self.close()
