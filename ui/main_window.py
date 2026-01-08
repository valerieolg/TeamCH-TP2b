from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

from db.database import Database
from ui.AddPosteWindow import AddPosteWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre
        self.setWindowTitle("Parc informatique")
        self.setMinimumSize(800, 450)

        # Créer le layout principal/global de la fenêtre
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Titre de la page
        titre = QLabel("Parc informatique")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #titre.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Tableau

        # Créer tableau qui affichera les postes informatiques
        self.table = QTableView()

        # Comportement d'utilisation du tableau

        # Toute la ligne est sélectionnée ensemble
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # Empêcher la sélection de plus qu'un poste en même temps
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # Interdire la modification des cellules directement dans le tableau
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Créer le modèle de données qui contiendra les postes, i.e. lien entre SQLite et QTableView
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Nom Poste","Utilisateur","Type Poste","System d'exploitation", "Adresse IP", "Statut"])

        # Associer le modèle à la table (le QTableView affichera automatiquement le contenu du modèle)
        self.table.setModel(self.model)

        # Ajuster automatiquement la largeur de la dernière colonne pour occuper tout l'espace horizontal
        self.table.horizontalHeader().setStretchLastSection(True)

        # Boutons

        # Créer layout horizontal de Qwidgets
        btn_layout = QHBoxLayout()

        # Créer les boutons et définir leur libellé
        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")
        btn_refresh = QPushButton("Actualiser")
        btn_quit = QPushButton("Quitter")

        # Lier les boutons aux méthodes appropriées
        btn_add.clicked.connect(self.open_add_window)
        btn_edit.clicked.connect(self.edit_poste)
        btn_delete.clicked.connect(self.delete_poste)
        btn_refresh.clicked.connect(self.load_postes_from_db)
        btn_quit.clicked.connect(self.close)

        # Ajouter les boutons au layout horizontal
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_quit)

        # Ajouter les widgets définis jusqu'à présent au layout global de la page
        main_layout.addWidget(titre)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)

        # Ajouter le layout global à la page (l'instance de MainWindow). C'est ce qui rend le layout visible et actif.
        self.setLayout(main_layout)

        # Référence vers la fenêtre "Ajouter / Modifier un poste?", pour l'associer à MainWindow
        # Initialisée à None pour permettre de, ailleurs dans le code, vérifier si la fenêtre existe ou non.
        self.add_window = None

        # Chargement initial des postes depuis la base de données SQLite
        # Cette méthode remplit le tableau dès l'ouverture de l'application
        self.load_postes_from_db()

    # Actions
    def open_add_window(self):
        # Instancie la fenêtre d'ajout de poste
        # La fonction load_postes_from_db est passée comme callback
        # afin de rafraîchir la QTableView après l'enregistrement en base SQLite
        self.add_window = AddPosteWindow(on_save_callback=self.load_postes_from_db)
        self.add_window.show()

    def edit_poste(self):
        index = self.table.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un poste à modifier."
            )
            return

        # Obtient l'indice de la ligne sélectionnée dans la QTableView
        row = index.row()

        # Extrait l'identifiant unique du poste depuis le modèle
        # Cet identifiant provient de la base SQLite et est stocké
        # dans la colonne "Nom" à l'aide du rôle UserRole
        id_poste = self.model.item(row, 0).data(Qt.ItemDataRole.UserRole)

        poste_data = (
            id_poste,
            self.model.item(row, 0).text(),
            self.model.item(row, 1).text(),
            self.model.item(row, 2).text(),
            self.model.item(row, 3).text()
        )

        # Instancie la fenêtre d'ajout/modification en mode édition
        # Les données du poste sélectionné sont passées afin de préremplir le formulaire
        # Un callback est fourni pour recharger les données après la mise à jour SQLite
        self.add_window = AddPosteWindow(poste_data=poste_data, on_save_callback=self.load_postes_from_db)
        self.add_window.show()

    def delete_poste(self):
        index = self.table.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un poste à supprimer."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce poste ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        # Vérifie si l'utilisateur a confirmé l'action de suppression
        if reply == QMessageBox.StandardButton.Yes:
            # Extraction de l'identifiant unique du poste depuis le modèle
            # Cet identifiant permet d'effectuer la suppression dans SQLite
            id_poste = self.model.item(index.row(), 0).data(Qt.ItemDataRole.UserRole)

            # Instanciation de la classe de gestion de la base de données
            db = Database()

            # Exécution de l'opération DELETE sur la table postes
            db.delete_poste(id_poste)

            self.load_postes_from_db()

    def load_postes_from_db(self):
        # Efface toutes les lignes du QStandardItemModel
        # Cette opération est nécessaire avant de recharger les données
        # depuis SQLite pour éviter les doublons dans la table
        self.model.removeRows(0, self.model.rowCount())
        db = Database()
        postes = db.get_all_postes()

        for poste in postes:
            id_poste, nom_poste, utilisateur, type_poste, sys_exploitation, adresse_ip, statut = poste

            row = [
                QStandardItem(id_poste),
                QStandardItem(nom_poste),
                QStandardItem(utilisateur),
                QStandardItem(type_poste),
                QStandardItem(sys_exploitation),
                QStandardItem(adresse_ip),
                QStandardItem(statut)
            ]

            # Stocker l'ID SQLite dans la première colonne
            row[0].setData(id_poste, Qt.ItemDataRole.UserRole)

            self.model.appendRow(row)


