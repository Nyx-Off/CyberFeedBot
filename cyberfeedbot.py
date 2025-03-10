#!/usr/bin/env python3

import feedparser
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import requests
from bs4 import BeautifulSoup

# Liste des liens RSS (incluant Infostealers et CS Hub)
rss_feeds = [
    "https://www.cert.ssi.gouv.fr/feed/",
    "https://www.cert.ssi.gouv.fr/feed/scada/",
    "https://msrc.microsoft.com/blog/categories/security-research-defense/feed",
    "https://msrc.microsoft.com/blog/categories/microsoft-threat-hunting/feed",
    "https://www.infostealers.com/info-stealers-reports/feed",
    "https://www.infostealers.com/learn-info-stealers/feed",
    "https://www.infostealers.com/info-stealers-techniques/feed"


]

# Fichier pour stocker les liens déjà envoyés
SENT_ARTICLES_FILE = "/usr/local/FluxRSS2/sent_articles.txt"

# Webhook Discord (remplacez par votre URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1287703661153222656/Y2GMhlZJX3jxXfc7-iVM-GjF3CN4qC97Ek1eRc-DH1oEmWjX2mYfNwaiRSgkrkHIrswC"

# ID du rôle à mentionner (remplacez par l'ID de votre rôle)
ROLE_ID = "1289149769528250410"

# Un header de base pour imiter un navigateur
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

# Pour CS Hub, ajouter un header Accept approprié
CSHUB_HEADERS = BASE_HEADERS.copy()
CSHUB_HEADERS.update({
    "Accept": "application/rss+xml, application/xml, text/xml"
})

print("-----------------------------------------------")
print("Script de notification d'articles de cybersécurité")
print("Date - Heure : {:%d/%m/%Y %H:%M}".format(datetime.now()))
print("-----------------------------------------------")

def load_sent_articles():
    if not os.path.exists(SENT_ARTICLES_FILE):
        return set()
    with open(SENT_ARTICLES_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_sent_article(link):
    with open(SENT_ARTICLES_FILE, "a") as f:
        f.write(link + "\n")

def send_discord_webhook(title, link, description, pub_date):
    published_date = parsedate_to_datetime(pub_date).strftime('%d/%m/%Y %H:%M')
    embed = {
        "title": title,
        "url": link,
        "description": description,
        "footer": {"text": f"Date: {published_date}"}
    }
    data = {
        "content": f"<@&{ROLE_ID}>",
        "embeds": [embed],
        "allowed_mentions": {"roles": [ROLE_ID]}
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code in (200, 204):
        print(f"Notification envoyée : {title}")
    else:
        print(f"Erreur lors de l'envoi de la notification pour : {title} (Code: {response.status_code})")

def is_today(pub_date):
    published_date = parsedate_to_datetime(pub_date).astimezone(timezone.utc).date()
    today = datetime.now(timezone.utc).date()
    return published_date == today

def parse_rss_feed(url, sent_articles):
    print(f"Traitement du flux : {url}")
    # Traitement pour Infostealers
    if "infostealers.com/" in url:
        response = requests.get(url, headers=BASE_HEADERS)
        if response.status_code != 200:
            print(f"Erreur lors du téléchargement du flux {url} : {response.status_code}")
            return False
        feed = feedparser.parse(response.text)
    # Traitement pour CS Hub
    elif "cshub.com/rss/articles" in url:
      # Utilisation de la méthode POST pour contourner l'erreur 405
      response = requests.request("POST", url, headers=CSHUB_HEADERS)
      if response.status_code != 200:
          print(f"Erreur lors du téléchargement du flux {url} : {response.status_code}")
          return False
      # Traitement du contenu via BeautifulSoup pour corriger d'éventuels problèmes de balisage
      soup = BeautifulSoup(response.content, "xml")
      feed = feedparser.parse(str(soup))
    else:
        feed = feedparser.parse(url)

    if feed.bozo:
        print(f"Erreur lors de l'analyse du flux {url} : {feed.bozo_exception}")
        return False

    articles_sent = False
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description_html = entry.description if 'description' in entry else 'Pas de description disponible'
        description = BeautifulSoup(description_html, 'html.parser').get_text()
        pub_date = entry.published if 'published' in entry else None

        if pub_date and is_today(pub_date):
            print(f"Article du jour trouvé : {title}")
            if link not in sent_articles:
                send_discord_webhook(title, link, description, pub_date)
                save_sent_article(link)
                articles_sent = True
            else:
                print(f"L'article a déjà été envoyé : {title}")
        else:
            print(f"L'article n'est pas d'aujourd'hui ou n'a pas de date de publication valide : {title}")
    return articles_sent

if __name__ == "__main__":
    sent_articles = load_sent_articles()
    any_articles_sent = False
    for rss_url in rss_feeds:
        articles_sent = parse_rss_feed(rss_url, sent_articles)
        if articles_sent:
            any_articles_sent = True
    if not any_articles_sent:
        print("Aucun nouvel article à envoyer pour le moment.")
