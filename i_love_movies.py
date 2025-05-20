import json
import os
import random
from datetime import datetime
from mastodon import Mastodon

mastodon = Mastodon(
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url='https://mastodon.social'
)

with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

def days_since(start_date_str):
    start = datetime.strptime(start_date_str, '%Y-%m-%d')
    return (datetime.utcnow() - start).days

def get_random_image():
    stills_dir = 'stills'
    allowed_exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(stills_dir) if f.lower().endswith(allowed_exts)]
    return os.path.join(stills_dir, random.choice(files)) if files else None

start_date = '2025-05-01'
day_count = days_since(start_date)

post = random.choice(posts)
quote = post.get('quote', '').strip()
comment = post.get('comment', '').strip()
title = post.get('title', '').strip()
hashtags = post.get('hashtags', [])

text = f"{quote} {comment}" if comment else quote
image = get_random_image()

if day_count % 30 == 0 and text and image:
    media = mastodon.media_post(image)
    main_status = mastodon.status_post(status=text, media_ids=[media])
elif day_count % 14 == 0 and title:
    main_status = mastodon.status_post(status=text)
    if hashtags:
        reply = f"{title} {' '.join(hashtags)}"
    else:
        reply = title
    mastodon.status_post(status=reply, in_reply_to_id=main_status['id'])
else:
    if random.choice([True, False]) and image:
        media = mastodon.media_post(image)
        mastodon.status_post(status='', media_ids=[media])
    elif text:
        mastodon.status_post(status=text)
