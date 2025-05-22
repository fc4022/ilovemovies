import json
import os
import random
from datetime import datetime
from mastodon import Mastodon

# Mastodon-Client einrichten
mastodon = Mastodon(
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url='https://mastodon.social'
)

# Posts aus JSON laden
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Bilder aus Ordner laden
stills_path = 'stills'
images = [f for f in os.listdir(stills_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Tageszähler seit Startdatum
start_date = datetime.strptime('2025-05-01', '%Y-%m-%d')
today = datetime.utcnow()
day_count = (today - start_date).days

# Index berechnen (rotierend durch die Liste)
post = posts[day_count % len(posts)]

# Sonderfall: alle 30 Tage – Bild posten mit zufälligem Kommentar
if day_count % 30 == 0:
    if not images:
        exit()
    img = random.choice(images)
    media = mastodon.media_post(os.path.join(stills_path, img), mime_type='image/jpeg')
    random_comment = random.choice([p.get('comment', '') for p in posts if p.get('comment', '').strip()])
    mastodon.status_post(status=random_comment, media_ids=[media])

# Alle 14 Tage: nur Zitat, mit oder ohne Hashtags, immer mit Titel als Reply
elif day_count % 14 == 0:
    quote = post.get('quote', '')
    hashtags = post.get('hashtags', '')
    title = post.get('title', '')

    if day_count % 28 == 0 and hashtags:
        status = mastodon.status_post(f"{quote} {hashtags}")
    else:
        status = mastodon.status_post(quote)

    if title:
        mastodon.status_post(status=title, in_reply_to_id=status['id'])

# Standard: Zitat + Kommentar posten
else:
    quote = post.get('quote', '')
    comment = post.get('comment', '')
    if quote and comment:
        mastodon.status_post(f"{quote} {comment}")
    else:
        mastodon.status_post(quote or comment)