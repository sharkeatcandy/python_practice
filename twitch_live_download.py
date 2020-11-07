import requests
import json
import re
import argparse
import random
import m3u8
import ffmpeg # https://pypi.org/project/ffmpeg-python/
from datetime import datetime

LIVE_API = 'http://usher.twitch.tv/api/channel/hls/{channel}.m3u8?' +\
    '&token={token}&sig={sig}&allow_audio_only=true&allow_source=true'
LIVE_TOKEN_API = 'http://api.twitch.tv/api/channels/{channel}/access_token?oauth_token={user_token}'

VOD_API = 'https://usher.ttvnw.net/vod/{vod_number}.m3u8?' +\
    '&token={token}&sig={sig}&allow_audio_only=true&allow_source=true'
VOD_TOKEN_API = 'http://api.twitch.tv/api/vods/{vod_number}/access_token?oauth_token={user_token}'

def get_live_token_and_signature(channel, user_token):
    url = LIVE_TOKEN_API.format(channel=channel, user_token=user_token)
    r = requests.get(url)
    txt = r.text
    data = json.loads(txt)
    sig = data['sig']
    token = data['token']
    return token, sig

def get_live_stream(channel, user_token):
    token, sig = get_live_token_and_signature(channel, user_token)
    url = LIVE_API.format(channel=channel, sig=sig, token=token)
    r = requests.get(url)
    m3u8_obj = m3u8.loads(r.text)
    return m3u8_obj

def get_vod_token_and_signature(vod_number, user_token):
    url = VOD_TOKEN_API.format(vod_number=vod_number, user_token=user_token)
    r = requests.get(url)
    txt = r.text
    data = json.loads(txt)
    sig = data['sig']
    token = data['token']
    return token, sig

def get_vod_stream(vod_number, user_token):
    token, sig = get_vod_token_and_signature(vod_number, user_token)
    url = VOD_API.format(vod_number=vod_number, token=token, sig=sig)
    r = requests.get(url)
    m3u8_obj = m3u8.loads(r.text)
    return m3u8_obj

def download_mp3(uri, channel_name):
    current_date = datetime.today().strftime('%Y%m%d')
    stream = ffmpeg.input(uri)
    stream = ffmpeg.output(stream, '{}_{}.mp3'.format(channel_name, current_date))
    ffmpeg.run(stream)

def download_mp4(uri, channel_name):
    current_date = datetime.today().strftime('%Y%m%d')
    stream = ffmpeg.input(uri)
    stream = ffmpeg.output(stream, '{}_{}.mp4'.format(channel_name, current_date))
    ffmpeg.run(stream)

def get_video_urls(m3u8_obj):
    if m3u8_obj.playlists:
        print("Video URLs (sorted by quality):")
        for p in  m3u8_obj.playlists:
            si = p.stream_info
            bandwidth = si.bandwidth/(1024)
            quality = p.media[0].name
            resolution = si.resolution if si.resolution else "?"
            uri = p.uri
            txt = "\n{} kbit/s ({}), resolution={}".format(bandwidth, quality, resolution)
            print(txt)
            print(len(txt)*"-")
            print(uri)
            if quality == "audio_only" or quality == "Audio Only":
                audio_uri = uri
            elif "source" in quality or 'chunked' in uri:
                source_uri = uri
        return source_uri, audio_uri
    else:
        print("No live video")
        return 0, 0

if __name__=="__main__":
    parser = argparse.ArgumentParser('get video url of twitch channel')
    parser.add_argument('channel_name')
    parser.add_argument('user_token')
    parser.add_argument('download')
    args = parser.parse_args()
    if not args.channel_name.isdecimal():
        m3u8_obj = get_live_stream(args.channel_name, args.user_token)
    else:
        m3u8_obj = get_vod_stream(args.channel_name, args.user_token)
    source_uri, audio_uri = get_video_urls(m3u8_obj)
    if args.download == 'mp3':
        download_mp3(audio_uri, args.channel_name)
    elif args.download == 'mp4':
        download_mp4(source_uri, args.channel_name)
    elif args.download != 'false':
        print('download argument only support "mp3" or "mp4"')