Application SmartHelp

## 1. Présentation du projet

**SmartHelp** est une application web de gestion des tickets d’incident de type Helpdesk. Elle vise à faciliter la déclaration, le suivi, la gestion et la résolution des incidents dans une organisation, en s’appuyant sur une gestion de rôles différenciée (Admin, Technicien, Utilisateur).

---

## 2. Objectifs

- Centraliser la gestion des incidents.
- Suivre l’état d’avancement des tickets.
- Générer des statistiques et des rapports dynamiques.
- Optimiser la répartition et le traitement des tickets par les techniciens.
- Offrir une interface simple et adaptée à chaque rôle.

---

## 3. Les rôles et leurs droits

### 3.1. Administrateur (Admin)
- Supervise tous les tickets, utilisateurs, techniciens.
- CRUD (Créer, Lire, Modifier, Supprimer) sur tous les tickets, utilisateurs, techniciens.
- Assigner des tickets aux techniciens.
- Visualiser des tableaux de bord dynamiques avec :
    - Diagrammes 360°
    - Statistiques sur les tickets (par statut, par technicien, par priorité, etc.)
    - Taux de résolution, temps moyen de traitement, etc.

### 3.2. Technicien
- Visualise uniquement les tickets qui lui sont assignés.
- Met à jour le statut de ses tickets (en cours, en attente, résolu, etc.).
- Accède à un dashboard dynamique :
    - Nombre de tickets en cours, résolus, en attente.
    - Evolution des tickets dans le temps, priorités, etc.

### 3.3. Utilisateur (User)
- Crée un ticket (description, pièce jointe, urgence, etc.).
- Consulte la liste de ses tickets.
- Voit l’état, à qui le ticket est assigné, les commentaires, l’historique des changements.
- Dashboard simple :
    - Tickets ouverts, en attente, résolus.
    - Historique personnel.

---

## 4. Fonctionnalités principales

### 4.1. Gestion des utilisateurs
- Inscription, connexion, gestion des profils.
- Attribution d’un rôle (admin, technicien, utilisateur).

### 4.2. Gestion des tickets
- Création de ticket (titre, description, catégorie, urgence, pièce jointe).
- Modification/suppression (par l’auteur ou l’admin selon le statut).
- Attribution manuelle/automatique à un technicien (par l’admin).
- Suivi des statuts : Ouvert, En cours, En attente, Résolu, Fermé.
- Historique des actions sur chaque ticket.
- Ajout de commentaires (utilisateur, technicien, admin).

### 4.3. Tableaux de bord & Statistiques
- Pour chaque rôle, dashboard personnalisé :
    - Graphiques circulaires, barres, timelines, etc.
    - Filtres par date, urgence, statut, technicien, etc.
- Export de rapports (PDF, CSV).

### 4.4. Notifications
- Email à la création, à l’affectation, à la résolution d’un ticket.
- Notifications internes (optionnel).

### 4.5. Sécurité & droits d’accès
- Authentification sécurisée (login/password, mot de passe oublié).
- Gestion des permissions par rôle.
- Journalisation des actions critiques.

---

## 5. Architecture technique

- **Framework** : Django (Python)
- **Base de données** : SQLite (défaut Django, évolutif vers PostgreSQL/MySQL)
- **Front-end** : Django templates, Bootstrap (ou autre framework CSS)
- **Librairie de graphiques** : Chart.js, Plotly.js ou autre pour dashboards dynamiques
- **Gestion des fichiers** : Stockage des pièces jointes sur le serveur
- **Envoi d’emails** : Configuration SMTP Django

---

## 6. Modèle de données (exemple simplifié)

- **User** : username, email, password, rôle (admin/technicien/utilisateur)
- **Ticket** : titre, description, date création, urgence, statut, auteur, technicien assigné, pièce jointe, historique
- **Commentaire** : ticket, auteur, texte, date
- **HistoriqueTicket** : ticket, action, auteur, date

---

## 7. Interfaces & UX

- Interfaces épurées et intuitives pour chaque rôle.
- Responsive design (mobile/desktop).
- Navigation fluide, recherche et filtres avancés.

---

## 8. Exigences non fonctionnelles

- Application multi-utilisateurs.
- Performances correctes pour une base de test (SQLite).
- Sécurité des données (mot de passe hashé, protection CSRF...).
- Code documenté et structuré (suivant les bonnes pratiques Django).


