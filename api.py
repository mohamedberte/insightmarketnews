from time import sleep
import requests
from requests_oauthlib import *
import textwrap

class XPostFinanceFeatures:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # Initialisation avec les clés OAuth
        self.oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )
        
    def __str__(self) -> str:
        # Décrire l'état de la classe
        return "Classe XPostFinanceFeatures pour interagir avec X (Twitter) via l'API"
    
    def test_authentication(self):
        # Effectuer une requête simple pour vérifier l'authentification
        url = "https://api.twitter.com/2/users/me"
        response = self.oauth.get(url)
        if response.status_code == 200:
            print("Authentification réussie.")
        else:
            raise Exception(f"Erreur d'authentification : {response.status_code} - {response.text}")

    def post_long_tweet(self, text):
        """Poster un tweet long en utilisant des threads"""
        if len(text) <= 275:
            # Si le texte est inférieur ou égal à 280 caractères, poster directement
            return self.post_tweet(text)
    
        # Diviser le texte en morceaux de 275 caractères sans couper les mots
        tweets = textwrap.wrap(text, width=275, break_long_words=False)
        tweets = [tweet + '...' if i < len(tweets) - 1 else tweet for i, tweet in enumerate(tweets)]
        
        # Poster le premier tweet
        response = self.post_tweet(tweets[0])
        if response.status_code != 201:
            raise Exception(f"Erreur lors de la publication du tweet: {response.status_code} {response.text}")
        
        # Récupérer l'ID du tweet initial
        tweet_id = response.json()['data']['id']
        sleep(2)
        # Poster les tweets suivants en réponse au premier tweet
        for tweet in tweets[1:]:
            response = self.reply_to_tweet(tweet, tweet_id=tweet_id)
            sleep(2)
        return response
    
    def post_tweet(self, text, in_reply_to_tweet_id=None):
        """Poster un tweet"""
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": text}
        if in_reply_to_tweet_id:
            payload["in_reply_to_tweet_id"] = in_reply_to_tweet_id
        response = self.oauth.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Erreur lors de la publication du tweet: {response.status_code} {response.text}")
        return response

    def retweet(self, tweet_id):
        """Retweeter un tweet spécifique"""
        url = f"https://api.twitter.com/2/users/{self.get_user_id()}/retweets"
        payload = {"tweet_id": tweet_id}
        
        response = self.oauth.post(url, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Erreur lors du retweet: {response.status_code} {response.text}")
        
        return response.json()

    def reply_to_tweet(self, text, tweet_id):
        """Répondre à un tweet spécifique"""
        url = "https://api.twitter.com/2/tweets"
        payload = {
            "text": text,
            "reply": {"in_reply_to_tweet_id": tweet_id}
        }
        
        response = self.oauth.post(url, json=payload)
        
        if response.status_code != 201:
            raise Exception(f"Erreur lors de la réponse: {response.status_code} {response.text}")
        
        return response.json()

    def like_tweet(self, tweet_id):
        """Aimer un tweet spécifique"""
        url = f"https://api.twitter.com/2/users/{self.get_user_id()}/likes"
        payload = {"tweet_id": tweet_id}
        
        response = self.oauth.post(url, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Erreur lors de l'ajout du like: {response.status_code} {response.text}")
        
        return response.json()

    def delete_tweet(self, tweet_id):
        """Supprimer un tweet spécifique"""
        url = f"https://api.twitter.com/2/tweets/{tweet_id}"
        
        response = self.oauth.delete(url)
        
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la suppression du tweet: {response.status_code} {response.text}")
        
        return response.json()

    def get_user_id(self, username="self"):
        """Obtenir l'ID de l'utilisateur authentifié ou d'un autre utilisateur"""
        if username == "self":
            url = "https://api.twitter.com/2/users/me"
        else:
            url = f"https://api.twitter.com/2/users/by/username/{username}"
        
        response = self.oauth.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération de l'ID utilisateur: {response.status_code} {response.text}")
        
        user_info = response.json()
        return user_info['data']['id']
    
    def get_followers(self, user_id, max_results=10):
        """Méthode pour récupérer les abonnés d'un utilisateur"""
        url = f"https://api.twitter.com/2/users/{user_id}/followers"
        params = {"max_results": max_results}  # Limite à 10 résultats par défaut
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des abonnés: {response.status_code} {response.text}")
        return response.json()

    def get_following(self, user_id, max_results=10):
        """Méthode pour récupérer les utilisateurs suivis par un utilisateur"""
        url = f"https://api.twitter.com/2/users/{user_id}/following"
        params = {"max_results": max_results}  # Limite à 10 résultats par défaut
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des utilisateurs suivis: {response.status_code} {response.text}")
        return response.json()

    def follow_user(self, user_id):
        """"Méthode pour suivre un utilisateur"""
        url = f"https://api.twitter.com/2/users/{self.get_user_id()}/following"
        payload = {"target_user_id": user_id}
        response = self.oauth.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Erreur lors du suivi de l'utilisateur: {response.status_code} {response.text}")
        return response.json()

    def unfollow_user(self, user_id):
        """Méthode pour ne plus suivre un utilisateur"""
        url = f"https://api.twitter.com/2/users/{self.get_user_id()}/following/{user_id}"
        response = self.oauth.delete(url)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de l'arrêt du suivi: {response.status_code} {response.text}")
        return response.json()

    def get_user_id(self, username="self"):
        """Méthode pour récupérer l'ID utilisateur (modifiée pour fonctionner avec followers)"""
        if username == "self":
            url = "https://api.twitter.com/2/users/me"
        else:
            url = f"https://api.twitter.com/2/users/by/username/{username}"
        response = self.oauth.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération de l'ID utilisateur: {response.status_code} {response.text}")
        user_info = response.json()
        return user_info['data']['id']
    
    def search_users(self, query, max_results=10):
        """Recherche d'utilisateurs par mot-clé"""
        url = f"https://api.twitter.com/2/users/by?usernames={query}"
        params = {"max_results": max_results}
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la recherche d'utilisateurs: {response.status_code} {response.text}")
        return response.json()

    def check_friendship(self, source_user_id, target_user_id):
        """Vérifier la relation d'amitié entre deux utilisateurs"""
        url = f"https://api.twitter.com/2/users/{source_user_id}/following/{target_user_id}"
        response = self.oauth.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la vérification de la relation: {response.status_code} {response.text}")
        return response.json()

    def get_user_tweets(self, user_id, max_results=10):
        """Obtenir les tweets récents d'un utilisateur"""
        url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {"max_results": max_results}
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des tweets: {response.status_code} {response.text}")
        return response.json()

    def get_mutual_followers(self, user_id):
        """Obtenir les abonnés en commun (qui suivent et sont suivis par l'utilisateur)"""
        followers = self.get_followers(user_id)
        following = self.get_following(user_id)
        mutual_followers = set(follower['id'] for follower in followers['data']) & set(follow['id'] for follow in following['data'])
        return list(mutual_followers)
    
    def get_mentions(self, max_results=10):
        """Obtenir les tweets qui mentionnent l'utilisateur authentifié"""
        user_id = self.get_user_id()
        url = f"https://api.twitter.com/2/users/{user_id}/mentions"
        params = {"max_results": max_results}
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des mentions: {response.status_code} {response.text}")
        return response.json()

    def get_liked_tweets(self, user_id, max_results=10):
        """Obtenir la liste des tweets aimés par un utilisateur"""
        url = f"https://api.twitter.com/2/users/{user_id}/liked_tweets"
        params = {"max_results": max_results}
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des tweets aimés: {response.status_code} {response.text}")
        return response.json()

    def get_trending_topics(self, location_id=1):
        """Obtenir les tendances dans une région spécifique (1 = Worldwide)"""
        url = f"https://api.twitter.com/1.1/trends/place.json?id={location_id}"
        response = self.oauth.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des tendances: {response.status_code} {response.text}")
        return response.json()

    def get_tweet_engagement(self, tweet_id):
        """Obtenir le nombre de retweets et de likes pour un tweet spécifique"""
        url = f"https://api.twitter.com/2/tweets/{tweet_id}"
        response = self.oauth.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération de l'engagement: {response.status_code} {response.text}")
        tweet_data = response.json()
        return {
            "retweet_count": tweet_data['data']['public_metrics']['retweet_count'],
            "like_count": tweet_data['data']['public_metrics']['like_count']
        }

    def search_hashtag_tweets(self, hashtag, max_results=10):
        """Obtenir des tweets contenant un certain hashtag"""
        url = f"https://api.twitter.com/2/tweets/search/recent?query=%23{hashtag}"
        params = {"max_results": max_results}
        response = self.oauth.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la recherche de tweets avec le hashtag: {response.status_code} {response.text}")
        return response.json()

    def get_tweet_info(self, tweet_id):
        """Obtenir des informations détaillées sur un tweet spécifique"""
        url = f"https://api.twitter.com/2/tweets/{tweet_id}"
        response = self.oauth.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des informations du tweet: {response.status_code} {response.text}")
        return response.json()

    def send_direct_message(self, recipient_id, text):
        """Envoyer un message direct à un utilisateur"""
        url = "https://api.twitter.com/2/direct_messages/events/new"
        payload = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {"recipient_id": recipient_id},
                    "message_data": {"text": text}
                }
            }
        }
        response = self.oauth.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Erreur lors de l'envoi du message: {response.status_code} {response.text}")
        return response.json()



# Class get data from rest api http post bedrock [AWS API Gateway]
class AwsApiGateWay:
    def __init__(self, url):
        self.url = url

    def post_data(self, data: str):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'post_brut': data
        }
        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de l'envoi des données: {response.status_code} {response.text}")
        return response.json()['body']