import os
import re
import time
import json
import urllib
import argparse
import datetime
from InstagramAPI import InstagramAPI

def download_post(api, post_id, save_dir):
    api.media_info(post_id)
    if api.LastJson['items'][0]['media_type'] == 1:
        image_url = api.LastJson['items'][0]['image_versions2']['candidates'][0]['url']
        filename = post_id + '.jpg'
        urllib.request.urlretrieve(image_url, os.path.join(save_dir, filename))
    elif api.LastJson['items'][0]['media_type'] == 2:
        video_url = api.LastJson['items'][0]['video_versions'][0]['url']
        filename = post_id + '.mp4'
        urllib.request.urlretrieve(video_url, os.path.join(save_dir, filename))
    else:
        print("Media type not supported.")

def download_posts(api, user_id, num_posts, save_dir):
    api.user_timeline(user_id)
    posts = api.LastJson['items'][:num_posts]
    for post in posts:
        post_id = post['id']
        download_post(api, post_id, save_dir)
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Instagram posts.')
    parser.add_argument('username', type=str, help='Instagram username')
    parser.add_argument('--num_posts', type=int, default=10, help='Number of posts to download (default: 10)')
    parser.add_argument('--save_dir', type=str, default='./downloads', help='Directory to save posts (default: ./downloads)')
    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    api = InstagramAPI(args.username)
    api.login()

    user_id = api.username_id
    download_posts(api, user_id, args.num_posts, args.save_dir)

    print('Download complete!')
