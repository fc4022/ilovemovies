import json
import os
import random
from datetime import datetime
from mastodon import Mastodon

# Mastodon-Setup
mastodon = Mastodon(
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url='https://mastodon.social'
)

# Load text posts
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Hilfsfunktionen
def days_since(start_date_str):
    start = datetime.strptime(start_date_str, '%Y-%m-%d')
    return (datetime.utcnow() - start).days

def get_random_image():
    allowed_exts = ('.jpg', '.jpeg', '.png', '.webp')
    stills_dir = 'stills'
    files = [f for f in os.listdir(stills_dir) if f.lower().endswith(allowed_exts)]
    return os.path.join(stills_dir, random.choice(files)) if files else None

# Startlogik
start_date = '2025-05-01'
day_count = days_since(start_date)

random_post = random.choice(posts)
random_image = get_random_image()

# 1x im Monat: Bild + Text (nicht zusammengehörig)
if day_count % 30 == 0 and random_image and random_post.get('quote', '').strip():
    media = mastodon.media_post(random_image)
    mastodon.status_post(status=random_post['quote'], media_ids=[media])

# Ansonsten: Nur Bild oder nur Text (abwechselnd, zufällig)
else:
    if random.choice([True, False]) and random_image:
        media = mastodon.media_post(random_image)
        mastodon.status_post(status='', media_ids=[media])
    elif random_post.get('quote', '').strip():
        mastodon.status_post(status=random_post['quote'])
