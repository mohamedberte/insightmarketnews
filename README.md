# Insight Market News

Votre source quotidienne d’analyses et d’actualités sur l’économie, la finance, la politique et la santé. Suivez nos insights pour des décisions plus éclairées.

## Objectif du Projet

Ce projet vise à extraire les tendances des cryptomonnaies et autres actifs financier depuis l'API CoinMarketCap et d'autres API, puis à synthétiser ces informations grâce à AWS Bedrock pour générer un post et le publier sur le compte Insight Market News (compte X). L'objectif est d'informer les utilisateurs des tendances des actifs.

## Fonctionnalités

- Extraction des données de tendances de cryptomonnaies via l'API CoinMarketCap.
- Utilisation d'AWS Bedrock pour l'analyse et la synthèse des données.
- Déploiement de fonctions AWS Lambda pour le traitement des données.
- Utilisation d'API Gateway pour gérer les requêtes et les réponses.
- Publication automatique des posts sur le compte Insight Market News.

## Technologies Utilisées

- **API CoinMarketCap** : Pour l'extraction des données de tendances des cryptomonnaies.
- **AWS Bedrock** : Pour l'analyse et la synthèse des données.
- **AWS Lambda** : Pour le traitement des données.
- **API Gateway** : Pour la gestion des requêtes et des réponses.
- **Compte X (anciennement Twitter)** : Pour la publication des posts.

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/username/insightmarketnews.git
    ```
2. Installez les dépendances nécessaires :
    ```bash
    cd insightmarketnews
    ```

## Utilisation

1. Configurez les clés API pour CoinMarketCap et API Twitter (X v2) dans le fichier `.env`.
2. Déployez les fonctions AWS Lambda :
    ```bash
    serverless deploy
    ```
3. Lancez l'application :
    ```bash
    npm start
    ```

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## Licence

Ce projet est sous licence Free. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Structure du Projet

```
__pycache__/
.env
.gitignore
api.py
knowledge/
    post/
        crypto_post_2025-02-02.txt
main.py
readMe.md
```

## Description des Fichiers

- `main.py` : Script principal pour l'extraction, l'analyse et la publication des données de performance des cryptomonnaies.
- `api.py` : Contient les classes pour interagir avec l'API X (anciennement Twitter) et AWS API Gateway.
- `knowledge/post/` : Contient les fichiers texte générés pour les posts quotidiens sur les performances des cryptomonnaies.
- `.env` : Fichier de configuration pour les clés API.
- `.gitignore` : Fichier pour ignorer les fichiers et dossiers spécifiques dans Git.
- `readMe.md` : Documentation du projet.

## Exécution du Script Principal

Le script principal `main.py` effectue les étapes suivantes :
1. Charge les variables d'environnement depuis le fichier `.env`.
2. Lit les données de performance des cryptomonnaies pour aujourd'hui et hier.
3. Trie les données pour obtenir les meilleures performances.
4. Prépare le texte du post à partir des données triées.
5. Sauvegarde le texte du post dans un fichier.
6. Publie le post sur le compte X via l'API.

## Exemple de Post Généré

```
🚀 Top 5 Crypto Performances Today (2025-02-04) 🚀

📊 Comparatif avec hier :
🔥 Bitcoin (BTC) maintient sa place en tête avec +5.2% aujourd’hui !
🎉 Solana (SOL) fait une entrée fracassante dans le top avec +8.4% !
⚠️ Ethereum (ETH) ralentit mais reste solide avec +2.1%.

🔹 Classement du jour :
1️⃣ Bitcoin (BTC) – +5.2% | $44,320 | Volume 24h : $25B
2️⃣ Solana (SOL) – +8.4% | $112.4 | Volume 24h : $8B
3️⃣ Ethereum (ETH) – +2.1% | $2,540 | Volume 24h : $15B
4️⃣ XRP (XRP) – +3.8% | $0.67 | Volume 24h : $3B
5️⃣ Cardano (ADA) – +4.5% | $0.52 | Volume 24h : $2B

📌 Le marché évolue vite, restez informés ! 📌
⚠️ Ceci n'est pas un conseil financier. Faites vos propres recherches avant d’investir.

#Crypto #TopPerformers #CryptoMarket #Bitcoin #Ethereum #Solana
----------------------------------
```