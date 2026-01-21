# 🎯 Gestion des Incidents - Module Odoo 17

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Odoo](https://img.shields.io/badge/Odoo-17.0-purple.svg)
![License](https://img.shields.io/badge/license-LGPL--3-green.svg)

## 📋 Description

Module Odoo 17 complet pour la gestion des incidents IT avec système de SLA, gestion d'équipes, base de connaissances et portail client intégré.

## ✨ Fonctionnalités Principales

### 🎫 Gestion des Incidents
- **Workflow complet** : Nouveau → En cours → Résolu → Fermé
- **Priorisation** : Basse, Normale, Haute, Urgente
- **Affectation automatique** aux équipes de support
- **Suivi détaillé** avec historique des modifications
- **Évaluation** de la résolution par les clients

### ⏱️ SLA (Service Level Agreement)
- **Définition de SLA** par priorité et catégorie
- **Alertes automatiques** de dépassement
- **Calcul en temps réel** du temps restant
- **Indicateurs visuels** de conformité

### 👥 Gestion des Équipes
- **Organisation par équipes** de support
- **Affectation de membres** et responsables
- **Spécialisation par catégories** d'incidents
- **Statistiques d'équipe** et charge de travail

### 📚 Base de Connaissances
- **Solutions réutilisables** pour incidents récurrents
- **Recherche intelligente** par mots-clés
- **Catégorisation** des articles
- **Statistiques d'utilisation** et popularité

### 🌐 Portail Client
- **Création d'incidents** en ligne
- **Suivi en temps réel** de l'avancement
- **Historique des incidents** personnalisé
- **Évaluation des résolutions**
- **Accès à la base de connaissances**

### 📊 Tableau de Bord
- **Vue d'ensemble** des incidents actifs
- **Graphiques interactifs** (pivot, graphique)
- **Indicateurs clés** de performance (KPI)
- **Filtres avancés** et recherche

## 🏗️ Structure du Module

```
incident_management/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── portal.py              # Contrôleurs portail client
├── data/
│   ├── demo_data.xml          # Données de démonstration
│   ├── sequence.xml           # Séquences automatiques
│   └── sla_data.xml           # SLA par défaut
├── models/
│   ├── __init__.py
│   ├── category.py            # Catégories d'incidents
│   ├── incident.py            # Modèle principal incidents
│   ├── knowledge.py           # Base de connaissances
│   ├── sla.py                 # Gestion SLA
│   └── team.py                # Équipes de support
├── security/
│   ├── ir.model.access.csv    # Droits d'accès
│   └── security.xml           # Groupes de sécurité
├── static/
│   └── src/
│       └── css/
│           └── incident_management.css
├── views/
│   ├── category_views.xml     # Vues catégories
│   ├── dashboard_views.xml    # Tableau de bord
│   ├── incident_views.xml     # Vues incidents
│   ├── knowledge_views.xml    # Vues base de connaissances
│   ├── menu.xml               # Menu principal
│   ├── portal_templates.xml   # Templates portail
│   ├── sla_views.xml          # Vues SLA
│   └── team_views.xml         # Vues équipes
└── README.md
```

## 🚀 Installation

### Prérequis
- Odoo 17.0
- Python 3.10+
- PostgreSQL 12+

### Étapes d'installation

1. **Cloner le dépôt**
   ```bash
   git clone <repository-url>
   cd GI-Odoo
   ```

2. **Démarrer avec Docker** (recommandé)
   ```bash
   docker-compose up -d
   ```

3. **Installation manuelle**
   - Copier le module dans le dossier `addons` d'Odoo
   - Redémarrer le serveur Odoo
   - Activer le mode développeur
   - Mettre à jour la liste des applications
   - Installer "Gestion des Incidents"

## 🔧 Configuration

### Configuration initiale

1. **Créer des catégories d'incidents**
   - Aller dans : Incidents → Configuration → Catégories
   - Exemples : Matériel, Logiciel, Réseau, Accès

2. **Définir les SLA**
   - Aller dans : Incidents → Configuration → SLA
   - Configurer les temps de réponse par priorité

3. **Créer des équipes de support**
   - Aller dans : Incidents → Configuration → Équipes
   - Assigner des membres et des catégories

4. **Configurer les groupes de sécurité**
   - Utilisateur : Peut créer et voir ses incidents
   - Agent : Peut traiter les incidents assignés
   - Manager : Accès complet et statistiques

## 👤 Groupes de Sécurité

| Groupe | Permissions |
|--------|-------------|
| **Utilisateur** | Créer des incidents, voir ses propres incidents, accès portail |
| **Agent Support** | Traiter les incidents assignés, accéder à la base de connaissances |
| **Manager** | Accès complet, configuration, statistiques, gestion des équipes |

## 📖 Utilisation

### Créer un incident

**Via l'interface Odoo :**
1. Aller dans Incidents → Incidents → Créer
2. Remplir les informations (titre, description, priorité, catégorie)
3. Sauvegarder

**Via le portail client :**
1. Se connecter au portail
2. Aller dans "Mes Incidents"
3. Cliquer sur "Créer un incident"

### Traiter un incident

1. Ouvrir l'incident depuis la liste
2. Changer le statut à "En cours"
3. Ajouter des notes dans le chatter
4. Lier un article de la base de connaissances si applicable
5. Marquer comme "Résolu" une fois terminé

### Consulter le tableau de bord

1. Aller dans Incidents → Tableau de bord
2. Visualiser les graphiques et statistiques
3. Utiliser les filtres pour analyser les données

## 🔌 API & Intégrations

Le module utilise les fonctionnalités standard d'Odoo :
- **API XML-RPC** pour intégrations externes
- **Webhooks** via le système de messagerie Odoo
- **Portail** pour accès client

## 🧪 Données de Démonstration

Le module inclut des données de démonstration :
- 3 catégories d'incidents
- 4 niveaux de SLA
- 2 équipes de support
- 5 incidents exemples
- 3 articles de base de connaissances

Pour charger les données de démo, installer le module avec les données de démonstration activées.

## 📊 Modèles de Données

### incident.incident
- `name` : Numéro unique (auto-généré)
- `title` : Titre de l'incident
- `description` : Description détaillée
- `priority` : Priorité (0-3)
- `state` : État (nouveau, en_cours, résolu, fermé)
- `category_id` : Catégorie
- `team_id` : Équipe assignée
- `user_id` : Agent assigné
- `partner_id` : Client
- `sla_id` : SLA applicable
- `deadline` : Date limite SLA

### incident.category
- `name` : Nom de la catégorie
- `description` : Description

### incident.sla
- `name` : Nom du SLA
- `priority` : Priorité concernée
- `response_time` : Temps de réponse (heures)

### incident.team
- `name` : Nom de l'équipe
- `leader_id` : Responsable
- `member_ids` : Membres
- `category_ids` : Catégories gérées

### incident.knowledge
- `title` : Titre de l'article
- `content` : Contenu
- `category_id` : Catégorie
- `keywords` : Mots-clés

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence LGPL-3. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteurs

**Projet TP Odoo - 5IIR**

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Contacter l'équipe de développement

## 🔄 Changelog

### Version 2.0
- ✅ Migration vers Odoo 17
- ✅ Ajout du portail client
- ✅ Système de SLA automatique
- ✅ Base de connaissances intégrée
- ✅ Tableau de bord amélioré
- ✅ Gestion des équipes

### Version 1.0
- ✅ Gestion basique des incidents
- ✅ Workflow de traitement
- ✅ Catégorisation

## 🎯 Roadmap

- [ ] Notifications par email automatiques
- [ ] Intégration avec outils externes (Slack, Teams)
- [ ] Rapports PDF personnalisables
- [ ] Application mobile
- [ ] Intelligence artificielle pour catégorisation automatique
- [ ] Chatbot de support

---

**Fait avec ❤️ pour la gestion efficace des incidents IT**
