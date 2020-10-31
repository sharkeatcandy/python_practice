import requests
import json
import re
import argparse
import random
import m3u8

USHER_API = 'http://usher.twitch.tv/api/channel/hls/{channel}.m3u8?' +\
    '&token={token}&sig={sig}&allow_audio_only=true&allow_source=true' + \
    '&type=any&p={random}'
TOKEN_API = 'http://api.twitch.tv/api/channels/{channel}/access_token?oauth_token={user_token}'

def get_token_and_signature(channel, user_token):
    url = TOKEN_API.format(channel=channel, user_token=user_token)
    r = requests.get(url)
    txt = r.text
    data = json.loads(txt)
    print(data)
    sig = data['sig']
    token = data['token']
    return token, sig

def get_live_stream(channel, user_token):
    token, sig = get_token_and_signature(channel, user_token)
    r = random.randint(0,1E7)
    url = USHER_API.format(channel=channel, sig=sig, token=token, random=r)
    r = requests.get(url)
    m3u8_obj = m3u8.loads(r.text)
    return m3u8_obj

def print_video_urls(m3u8_obj):
    print("Video URLs (sorted by quality):") 
    for p in m3u8_obj.playlists:
        si = p.stream_info
        bandwidth = si.bandwidth/(1024)
        quality = p.media[0].name
        resolution = si.resolution if si.resolution else "?"
        uri = p.uri
        txt = "\n{} kbit/s ({}), resolution={}".format(bandwidth, quality, resolution)
        print(txt)
        print(len(txt)*"-")
        print(uri)

if __name__=="__main__":
    parser = argparse.ArgumentParser('get video url of twitch channel')
    parser.add_argument('channel_name')
    parser.add_argument('user_token')
    args = parser.parse_args()
    m3u8_obj = get_live_stream(args.channel_name, args.user_token)
    print_video_urls(m3u8_obj)
