
<div align="center">
  
# 🤖 CyberFeedBot

</div>

---

## 📌 À propos

CyberFeedBot est votre assistant de veille en cybersécurité. Il surveille automatiquement les flux RSS des sources les plus fiables et vous notifie en temps réel sur Discord. Fini les informations manquées, restez à jour sans effort !

### 🌟 Points Forts

- **Temps réel** : Notifications instantanées des nouvelles publications
- **Anti-spam** : Système intelligent de détection des doublons
- **Installation rapide** : Opérationnel en moins de 5 minutes
- **Personnalisable** : Ajoutez vos propres sources facilement

## 📊 Sources Surveillées

| Source | Catégorie | Fréquence |
|--------|-----------|-----------|
| 🛡️ CERT-FR | Alertes & Avis | Temps réel |
| 🏭 CERT-FR SCADA | Systèmes industriels | Temps réel |
| 🪟 Microsoft Security | Recherche & Défense | Quotidien |
| 🎯 Microsoft Threat Hunting | Menaces & Détection | Quotidien |
| 🕷️ Info-Stealer by HudsonRock | report - articles - technique | Quotidien |

## 🚀 Installation

```bash
# 1. Clonez le repository
git clone https://github.com/votrenomdutilisateur/cyberfeedbot

# 2. Accédez au dossier
cd cyberfeedbot

# 3. Installez les dépendances
pip install -r requirements.txt

# 4. Configurez vos variables
cp .env.example .env
# Éditez le fichier .env avec vos informations

# 5. Lancez le bot
python3 cyberfeedbot.py
```

## ⚙️ Configuration

### Prérequis

- Python 3.7 ou supérieur
- Un serveur Discord avec les droits d'administrateur
- Les dépendances Python suivantes :
  ```python
  feedparser~=6.0.10
  requests~=2.31.0
  beautifulsoup4~=4.12.2
  ```

### Configuration Discord

1. Dans votre serveur Discord :
   ```markdown
   1. Paramètres du serveur → Intégrations → Créer un Webhook
   2. Copier l'URL du Webhook
   3. Créer un rôle pour les notifications
   4. Copier l'ID du rôle (Clic droit → Copier l'ID)
   ```

2. Dans le script :
   ```python
   WEBHOOK_URL = "votre-url-webhook"
   ROLE_ID = "votre-id-role"
   ```

## 🔄 Automatisation

### Configuration Cron (Linux/Mac)

```bash
# Exécution toutes les heures
0 * * * * /usr/bin/python3 /chemin/vers/cyberfeedbot/cyberfeedbot.py

# Exécution toutes les 30 minutes
*/30 * * * * /usr/bin/python3 /chemin/vers/cyberfeedbot/cyberfeedbot.py
```


## 🛠️ Personnalisation

Ajoutez vos propres sources RSS :

```python
rss_feeds = [
    "https://votre-source-rss.com/feed",
    # Ajoutez d'autres flux ici
]
```

## 🤝 Contribution

Votre aide est la bienvenue ! Voici comment contribuer :

1. 🔀 Forkez le projet
2. 🌿 Créez une branche (`git checkout -b feature/AjoutSuperFonctionnalite`)
3. ✏️ Committez vos changements (`git commit -m 'Ajout d'une super fonctionnalité'`)
4. 📤 Pushez votre branche (`git push origin feature/AjoutSuperFonctionnalite`)
5. 📩 Ouvrez une Pull Request

## 📝 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 👥 Contact

- Créé par : [Nyx-Off]
---

<div align="center">

**🌟 N'oubliez pas de mettre une étoile si ce projet vous a été utile !**

</div>
