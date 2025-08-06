# Discord Bot & Rich Presence Manager Advanced

Une application complète en Python avec interface graphique pour gérer votre bot Discord et votre Rich Presence avec gestion d'assets intégrée.

## ✨ Fonctionnalités

### 🎮 Rich Presence
- Configuration complète du statut Discord
- Gestion des images (grande et petite)
- Affichage du temps écoulé
- Mise à jour automatique en temps réel
- Interface intuitive avec aperçu visuel

### 🤖 Bot Manager
- Changement du nom du bot en temps réel
- Modification de l'avatar du bot
- Gestion sécurisée des tokens
- Validation automatique des credentials

### 🖼️ Assets Manager
- Sauvegarde locale des assets
- Preview des images avant ajout
- Gestion des fichiers (max 8MB)
- Instructions intégrées pour Discord Developer Portal

## 📋 Prérequis

- Python 3.7 ou supérieur
- Compte Discord Developer
- Application Discord créée sur le Developer Portal

## 🚀 Installation

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/discord-manager-advanced.git
cd discord-manager-advanced
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

Ou installer manuellement :
```bash
pip install pypresence requests pillow
```

### 3. Lancer l'application
```bash
python discord_manager_advanced.py
```

## 📦 Dépendances

- **pypresence** - Pour la gestion du Rich Presence Discord
- **requests** - Pour les appels API Discord
- **Pillow (PIL)** - Pour la gestion des images
- **tkinter** - Interface graphique (inclus avec Python)

## 🔧 Configuration

### Discord Developer Portal

1. Rendez-vous sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application ou sélectionnez une existante
3. Notez l'**Application ID** (Client ID)
4. Si vous voulez utiliser le Bot Manager :
   - Allez dans l'onglet "Bot"
   - Créez un bot si nécessaire
   - Copiez le **Token** (gardez-le secret !)

### Premier démarrage

1. **Onglet Rich Presence** :
   - Entrez votre Application ID/Client ID
   - Configurez votre statut
   - Cliquez sur "Connecter RPC"

2. **Onglet Bot Manager** :
   - Entrez votre token bot
   - Modifiez le nom/avatar selon vos besoins

3. **Onglet Assets Manager** :
   - Ajoutez vos images localement
   - Suivez les instructions pour les uploader sur Discord

## 📱 Interface

L'application dispose de trois onglets principaux :

### 🎮 Rich Presence
- Configuration du Client ID
- Personnalisation des textes (détails, état)
- Gestion des images (grande/petite + textes de survol)
- Options d'affichage (temps écoulé)
- Connexion/déconnexion RPC

### 🤖 Bot Manager  
- Authentification sécurisée par token
- Modification du nom du bot
- Changement de l'avatar
- Status de connexion en temps réel

### 🖼️ Assets Manager
- Ajout d'assets avec preview
- Liste des assets sauvegardés
- Gestion locale des fichiers
- Instructions pour Discord Developer Portal

## 📁 Structure des fichiers

```
discord-rpc/
│
├── main.py    # Application principale
├── advanced_rpc_config.json       # Configuration sauvegardée (création automatique)
├── local_assets.json              # Assets locaux (création automatique)
├── assets/                        # Dossier des images d'assets (création automatique)
├── requirements.txt               # Dépendances Python
└── README.md                      # Ce fichier
```

## ⚙️ Configuration avancée

### Fichiers de configuration

- `advanced_rpc_config.json` : Sauvegarde automatique des paramètres RPC
- `local_assets.json` : Base de données locale des assets

### Personnalisation des couleurs

Vous pouvez modifier le thème de l'application en éditant les couleurs dans la méthode `setup_window()` :

```python
self.colors = {
    'bg': '#2C2F33',           # Arrière-plan principal
    'card': '#36393F',         # Arrière-plan des cartes
    'accent': '#7289DA',       # Couleur d'accent Discord
    'success': '#43B581',      # Vert de succès
    'danger': '#F04747',       # Rouge d'erreur
    'warning': '#FAA61A',      # Orange d'avertissement
    'text': '#FFFFFF',         # Texte principal
    'text_muted': '#B9BBBE'    # Texte secondaire
}
```

## 🛡️ Sécurité

- ⚠️ **IMPORTANT** : Ne partagez JAMAIS votre token de bot
- Les tokens ne sont pas sauvegardés dans les fichiers de configuration
- Utilisez des tokens de test pour le développement
- Révoquezz vos tokens si vous suspectez une compromission

## 🐛 Dépannage

### Problèmes courants

**RPC ne se connecte pas :**
- Vérifiez que Discord est ouvert
- Confirmez que l'Application ID est correct
- Vérifiez votre connexion internet

**Bot Manager ne fonctionne pas :**
- Vérifiez la validité du token
- Assurez-vous d'avoir les permissions nécessaires
- Vérifiez que le bot existe dans votre application

**Images d'assets trop grandes :**
- La limite Discord est de 8MB par image
- Utilisez des formats optimisés (PNG, JPG)
- Redimensionnez vos images si nécessaire

### Logs et débogage

Pour activer le mode debug, ajoutez ces lignes au début du script :

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 🙏 Remerciements

- [Discord](https://discord.com/) pour leur API et documentation
- [pypresence](https://github.com/qwertyquerty/pypresence) pour la librairie RPC
- La communauté Python pour les outils et librairies

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez la section [Dépannage](#-dépannage)
2. Consultez les [Issues](https://github.com/PainFromage/discord-rpc/issues)
3. Créez une nouvelle issue avec :
   - Description détaillée du problème
   - Steps de reproduction
   - Screenshots si applicable
   - Informations système (Python version, OS)

## 🔄 Changelog

### v1.0.0 (Date actuelle)
- 🎉 Version initiale
- ✅ Rich Presence complet
- ✅ Bot Manager fonctionnel  
- ✅ Assets Manager local
- ✅ Interface utilisateur moderne
- ✅ Sauvegarde automatique des configurations
**Fait avec ❤️ par [Votre nom]**

> ⭐ N'oubliez pas de star ce projet si il vous a aidé !
