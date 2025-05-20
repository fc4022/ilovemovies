import json
import os
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

start_date = datetime.strptime('2025-05-01', '%Y-%m-%d')
today = datetime.utcnow()
day_count = (today - start_date).days

max_text_posts = 90

text_index_file = 'text_index.txt'
reply_index_file = 'reply_index.txt'
image_index_file = 'image_index.txt'

text_index = load_index(text_index_file)
reply_index = load_index(reply_index_file)
image_index = load_index(image_index_file)

if text_index >= max_text_posts:
    # Keine weiteren Posts mehr
    exit()

if day_count % 30 == 0:
    # Bild + Quote posten (wenn möglich)
    while image_index < len(posts):
        post = posts[image_index]
        image_index += 1
        save_index(image_index_file, image_index)
        if post['image'] and post['quote']:
            media = mastodon.media_post(os.path.join('stills', post['image']), mime_type='image/jpeg')
            status = mastodon.status_post(status=post['quote'], media_ids=[media])
            if post['comment']:
                mastodon.status_post(status=post['comment'], in_reply_to_id=status['id'])
            break
elif day_count % 14 == 0:
    # Reply posten
    while reply_index < len(posts):
        post = posts[reply_index]
        reply_index += 1
        save_index(reply_index_file, reply_index)
        if post['comment']:
            text = post.get('film', post['comment'].strip('()'))
            hashtag = post.get('hashtag', '')
            if hashtag:
                text += ' ' + hashtag
            mastodon.status_post(text)
            break
else:
    # Täglichen Textpost ohne Wiederholung
    if text_index < len(posts):
        post = posts[text_index]
        if post['quote']:
            mastodon.status_post(post['quote'])
        text_index += 1
        save_index(text_index_file, text_index)