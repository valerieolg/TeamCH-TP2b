<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">


</head>
<body>

<h1>Parc informatique – Gestion des postes</h1>
<img src="README images/5.png" alt="" width="802" height="482">
<h2 id="description">Description</h2>
<p>
Application Python développée en <strong>programmation orientée objet (POO)</strong>
permettant la gestion complète d’un parc informatique à l’aide d’une interface graphique
réalisée avec <strong>PyQt6</strong> et d’une base de données <strong>SQLite</strong>.
</p>
<div class="sidebar">
    <ul>
        <li><a href="#fonctions">Fonctionnalités principales</a></li>
        <li><a href="#architecture">Architecture et conception</a></li>
        <li><a href="#validation">Validation</a></li>
        <li>
            <a href="#exemples">Exemples</a>
            <ul>
                <li><a href="#menu">Menu</a></li>
                <li><a href="#ajout">Ajout d'un poste</a></li>
                <li><a href="#modifier">Modification d'un poste</a></li>
                <li><a href="#supprimer">Suppression d'un poste</a></li>
                <li><a href="#rafraichir">Rafraîchir</a></li>
                <li><a href="#apropos">À propos</a></li>
            </ul>
        </li>
    </ul>
</div>
<h3 id="fonctions">Fonctionnalités principales</h3>
<ul>
    <li>Ajout de postes informatiques</li>
    <li>Modification de postes existants</li>
    <li>Suppression sécurisée de postes</li>
    <li>Validation centralisée des données</li>
    <li>Retour visuel immédiat en cas d’erreur</li>
    <li>Mise en évidence du champ invalide (bordure rouge)</li>
    <li>Placement automatique du curseur sur le champ en erreur</li>
    <li>Messages d’erreur explicites</li>
    <li>Persistance des données via SQLite</li>
</ul>

<p>
<strong>Concepts utilisés :</strong><br>
Encapsulation, séparation des responsabilités, validation centralisée des données,
programmation orientée objet.
</p>

<p>
<strong>Technologies et modules utilisés :</strong><br>
PyQt6, SQLite, re (expressions régulières), ipaddress.
</p>

<hr>

<h2 id="architecture">Architecture et conception</h2>

<h3>MainWindow</h3>
<p>
Classe principale de l’application.
Elle affiche la liste des postes informatiques à l’aide d’une <code>QTableView</code>
et permet l’accès aux fonctionnalités principales.
</p>
<ul>
    <li>Affichage du parc informatique</li>
    <li>Ajout, modification et suppression de postes</li>
    <li>Rafraîchissement des données depuis SQLite</li>
    <li>Gestion de la sélection des lignes</li>
</ul>

<h3>AddPosteWindow</h3>
<p>
Classe responsable de l’interface graphique permettant l’ajout et la modification
d’un poste informatique.
</p>
<ul>
    <li>Affichage des champs de saisie (QLineEdit, QComboBox)</li>
    <li>Gestion des boutons Enregistrer / Annuler</li>
    <li>Validation des champs via la classe <code>Catch</code></li>
    <li>Mise en évidence visuelle des champs invalides</li>
    <li>Positionnement automatique du focus sur le champ en erreur</li>
</ul>

<h3>Poste</h3>
<p>
Classe représentant un poste informatique.
Elle encapsule les attributs suivants :
</p>
<ul>
    <li>nom_poste</li>
    <li>utilisateur</li>
    <li>type_poste</li>
    <li>sys_exploitation</li>
    <li>adresse_ip</li>
    <li>statut</li>
</ul>

<h3>Database</h3>
<p>
Classe responsable de l’accès à la base de données SQLite.
Elle centralise toutes les opérations SQL.
</p>
<ul>
    <li>Ajout d’un poste</li>
    <li>Modification d’un poste existant</li>
    <li>Suppression d’un poste</li>
    <li>Lecture complète du parc informatique</li>
    <li>Isolation de la logique SQL</li>
</ul>

<h3>Catch (Validation des entrées)</h3>
<p>
Classe dédiée à la validation des données utilisateur.
Toutes les règles de validation sont centralisées afin de garantir
la cohérence, la maintenabilité et la robustesse du code.
</p>

<hr>

<h2 id="validation">Validation des champs</h2>

<h3>Nom du poste</h3>
<ul>
    <li>Obligatoire</li>
    <li>Accepte lettres, chiffres, accents, espaces, tirets et underscores</li>
    <li>Exemples valides : <em>PC-ADMIN</em>, <em>POSTE_01</em></li>
</ul>

<h3>Utilisateur</h3>
<ul>
    <li>Obligatoire</li>
    <li>Accepte lettres, chiffres, points, tirets et underscores</li>
    <li>Exemple valide : <em>jdupont</em></li>
</ul>

<h3>Type de poste</h3>
<ul>
    <li>Obligatoire</li>
    <li>Accepte lettres, chiffres, espaces et tirets</li>
    <li>Exemples : <em>Portable</em>, <em>Station de travail</em></li>
</ul>

<h3>Système d’exploitation</h3>
<ul>
    <li>Obligatoire</li>
    <li>Accepte lettres, chiffres, points et tirets</li>
    <li>Exemples : <em>Windows 10</em>, <em>Ubuntu 22.04</em></li>
</ul>

<h3>Adresse IP</h3>
<ul>
    <li>Obligatoire</li>
    <li>Doit respecter le format IPv4 valide</li>
    <li>Exemple : <em>192.168.1.10</em></li>
</ul>

<h3>Statut</h3>
<ul>
    <li>Valeur choisie dans une liste prédéfinie</li>
    <li>Valeurs autorisées : Actif, En réparation, Hors service</li>
</ul>
<h3>Exemple d'entrée de valeurs incorrectes</h3>
<ul>
    <img src="README images/11.png" alt="" width="422" height="323"><br>
    <img src="README images/12.png" alt="" width="422" height="323"><br>
    <img src="README images/13.png" alt="" width="422" height="323">
</ul>
<hr>

<h2 id="exemples">Exemples d’utilisation</h2>

<h3 id="menu">Menu principal</h3>
<ul>
    <li>Ajouter</li>
    <li>Modifier</li>
    <li>Supprimer</li>
    <li>Actualiser</li>
    <li>Quitter</li>
    <img src="README images/1.png" alt="" width="802" height="482"><br>
</ul>

 <h3 id="ajout">Ajout d’un poste</h3>
<ul>
    <li>Le champ concerné est encadré en rouge</li>
    <li>Le focus est automatiquement placé dessus</li>
    <li>Un message d’erreur explicatif est affiché</li>

<img src="README images/2.png" alt="" width="422" height="323"><br>
<img src="README images/3.png" alt="" width="422" height="323"><br>
<img src="README images/4.png" alt="" width="422" height="323"><br>
<img src="README images/5.png" alt="" width="802" height="482">
</ul>

<h3 id="modifier">Modification d’un poste</h3>
<p>
L’utilisateur sélectionne un poste existant dans la liste.
Les données sont préchargées dans le formulaire afin d’être modifiées.
Après validation, les changements sont enregistrés dans la base de données.
</p>
<img src="README images/7.png" alt="" width="802" height="482"><br>
<img src="README images/6.png" alt="" width="422" height="323"><br>
<img src="README images/9.png" alt="" width="422" height="323"><br>
<img src="README images/10.png" alt="" width="802" height="482"><br>

<h3 id="supprimer">Suppression d’un poste</h3>
<p>
L’utilisateur doit sélectionner un poste avant de confirmer sa suppression.
L’enregistrement est ensuite supprimé définitivement de la base SQLite.
</p>
<img src="README images/7.png" alt="" width="802" height="482"><br>
<img src="README images/8.png" alt="" width="802" height="482"><br>
<img src="README images/1.png" alt="" width="802" height="482"><br>


<h3 id="rafraichir">Rafraîchir</h3>
    <p>Recharge la liste complète des postes depuis la base de données.</p>

<h3 id="apropos">À propos</h3>
<p>
Le bouton "Aide et à propos de" ramène à une page HTML expliquant le fonctionnement du programme, aux remerciements et à nos contacts.<br>
<img src="README images/15.png" alt="" width="952" height="876">
</p>
<hr>
<p>
Projet réalisé par Valérie Ouellet dans le cadre du cours
<strong>420-2PR-BB – Programmation orientée objet</strong>,
Collège Bois-de-Boulogne – 2026.
</p>

</body>
</html>
