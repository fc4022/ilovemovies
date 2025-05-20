import json
import os
import random
from datetime import datetime
from mastodon import Mastodon

def load_index(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return int(f.read().strip())
    return 0

def save_index(file, index):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(index))

mastodon = Mastodon(
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url='https://mastodon.social'
)

with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

stills_path = 'stills'
images = [f for f in os.listdir(stills_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

start_date = datetime.strptime('2025-05-01', '%Y-%m-%d')
today = datetime.utcnow()
day_count = (today - start_date).days

text_index_file = 'text_index.txt'
reply_index_file = 'reply_index.txt'

text_index = load_index(text_index_file)
reply_index = load_index(reply_index_file)

if text_index >= len(posts):
    exit()

if day_count % 30 == 0:
    if not images:
        exit()
    img = random.choice(images)
    media = mastodon.media_post(os.path.join(stills_path, img), mime_type='image/jpeg')
    random_comment = random.choice([p.get('comment', '') for p in posts if p.get('comment', '').strip()])
    mastodon.status_post(status=random_comment, media_ids=[media])

elif day_count % 14 == 0:
    if reply_index >= len(posts):
        exit()
    post = posts[reply_index]
    reply_index += 1
    save_index(reply_index_file, reply_index)
    quote = post.get('quote', '')
    hashtags = post.get('hashtag', '')
    if reply_index % 2 == 0 and hashtags:
        mastodon.status_post(f"{quote} {hashtags}")
    else:
        mastodon.status_post(quote)

else:
    post = posts[text_index]
    text_index += 1
    save_index(text_index_file, text_index)
    quote = post.get('quote', '')
    comment = post.get('comment', '')
    if quote and comment:
        mastodon.status_post(f"{quote} {comment}")
    else:
        mastodon.status_post(quote or comment)