#!/usr/bin/env python3

import feedparser
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import requests
from bs4 import BeautifulSoup

# Liste des liens RSS
rss_feeds = [

    "https://www.cert.ssi.gouv.fr/feed/",
    "https://www.cert.ssi.gouv.fr/feed/scada/",
    "https://msrc.microsoft.com/blog/categories/security-research-defense/feed",
    "https://msrc.microsoft.com/blog/categories/microsoft-threat-hunting/feed",
    "https://www.cshub.com/rss/articles",

]

# Fichier pour stocker les liens des articles déjà envoyés
SENT_ARTICLES_FILE = "sent_articles.txt"

# Webhook Discord (remplacez par votre propre URL de webhook)
WEBHOOK_URL = ""

# ID du rôle à mentionner (remplacez par l'ID de votre rôle Discord)
ROLE_ID = ""

print("-----------------------------------------------")
print("Script de notification d'articles de cybersécurité")
print("Date - Heure : {:%d/%m/%Y %H:%M}".format(datetime.now()))
print("-----------------------------------------------")

def load_sent_articles():
    """Charge les liens des articles déjà envoyés à partir du fichier."""
    if not os.path.exists(SENT_ARTICLES_FILE):
        return set()
    with open(SENT_ARTICLES_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_sent_article(link):
    """Ajoute un nouveau lien d'article envoyé au fichier."""
    with open(SENT_ARTICLES_FILE, "a") as f:
        f.write(link + "\n")

def send_discord_webhook(title, link, description, pub_date):
    """Envoie un embed formaté via le webhook Discord."""
    # Formater la date de publication
    published_date = parsedate_to_datetime(pub_date).strftime('%d/%m/%Y %H:%M')

    # Créer l'embed
    embed = {
        "title": title,
        "url": link,
        "description": description,
        "footer": {
            "text": f"Date: {published_date}"
        }
    }
    # Payload
    data = {
        "content": f"<@&{ROLE_ID}>",  # Mentionner le rôle
        "embeds": [embed],
        "allowed_mentions": {
            "roles": [ROLE_ID]
        }
    }
    # Envoyer la requête POST au webhook Discord
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code in (200, 204):
        print(f"Notification envoyée : {title}")
    else:
        print(f"Erreur lors de l'envoi de la notification pour : {title} (Code: {response.status_code})")

def is_today(pub_date):
    """Vérifie si l'article a été publié aujourd'hui."""
    # Convertir la date de publication en objet datetime avec fuseau horaire
    published_date = parsedate_to_datetime(pub_date).astimezone(timezone.utc).date()

    # Obtenir la date actuelle avec fuseau horaire (UTC)
    today = datetime.now(timezone.utc).date()

    # Retourner True si l'article est publié aujourd'hui
    return published_date == today

def parse_rss_feed(url, sent_articles):
    """Analyse un flux RSS et envoie les nouveaux articles du jour."""
    print(f"Traitement du flux : {url}")
    feed = feedparser.parse(url)
    if feed.bozo:
        print(f"Erreur lors de l'analyse du flux {url} : {feed.bozo_exception}")
        return False  # Aucun article envoyé
    articles_sent = False  # Indicateur pour savoir si des articles ont été envoyés
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description_html = entry.description if 'description' in entry else 'Pas de description disponible'

        # Supprimer les balises HTML de la description
        soup = BeautifulSoup(description_html, 'html.parser')
        description = soup.get_text()

        pub_date = entry.published if 'published' in entry else None

        # Si l'article a une date de publication et qu'il est d'aujourd'hui
        if pub_date and is_today(pub_date):
            print(f"Article du jour trouvé : {title}")
            # Si l'article n'a pas encore été envoyé, on l'envoie et on l'enregistre
            if link not in sent_articles:
                send_discord_webhook(title, link, description, pub_date)
                save_sent_article(link)
                articles_sent = True
            else:
                print(f"L'article a déjà été envoyé : {title}")
        else:
            print(f"L'article n'est pas d'aujourd'hui ou n'a pas de date de publication valide : {title}")
    return articles_sent  # Retourne True si au moins un article a été envoyé

if __name__ == "__main__":
    # Charger les articles déjà envoyés
    sent_articles = load_sent_articles()
    any_articles_sent = False  # Indicateur global pour savoir si des articles ont été envoyés

    # Parcourir les flux RSS
    for rss_url in rss_feeds:
        articles_sent = parse_rss_feed(rss_url, sent_articles)
        if articles_sent:
            any_articles_sent = True

    if not any_articles_sent:
        print("Aucun nouvel article à envoyer pour le moment.")
