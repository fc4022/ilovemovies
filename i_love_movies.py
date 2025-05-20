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

start_date = '2025-05-01'
day_count = days_since(start_date)

post = random.choice(posts)
has_image = post.get('image', '').strip() != ''
has_text = post.get('quote', '').strip() != ''
has_comment = post.get('comment', '').strip() != ''

if day_count % 14 == 0 and has_image and has_text:
    media = mastodon.media_post(os.path.join('stills', post['image']), mime_type='image/jpeg')
    status = mastodon.status_post(status=post['quote'], media_ids=[media])
    if day_count % 30 == 0 and has_comment:
        mastodon.status_post(status=post['comment'], in_reply_to_id=status['id'])

elif day_count % 30 == 0 and has_text and has_comment and not has_image:
    text = f"{post['quote']} {post['comment']}"
    mastodon.status_post(status=text)

else:
    if has_image and not has_text:
        media = mastodon.media_post(os.path.join('stills', post['image']), mime_type='image/jpeg')
        mastodon.status_post(status='', media_ids=[media])
    elif has_text and not has_image:
        mastodon.status_post(status=post['quote'])
