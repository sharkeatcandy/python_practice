import argparse
import ffmpeg  # https://pypi.org/project/ffmpeg-python/
import json
import m3u8
import requests
import time
from datetime import datetime

TOKEN_QUERY = '{{"operationName":"PlaybackAccessToken_Template","query":"query PlaybackAccessToken_Template($login: String\u0021, $isLive: Boolean\u0021, $vodID: ID\u0021, $isVod: Boolean\u0021, $playerType: String\u0021) {{  streamPlaybackAccessToken(channelName: $login, params: {{platform: \\"web\\", playerBackend: \\"mediaplayer\\", playerType: $playerType}}) @include(if: $isLive) {{    value    signature    __typename  }}  videoPlaybackAccessToken(id: $vodID, params: {{platform: \\"web\\", playerBackend: \\"mediaplayer\\", playerType: $playerType}}) @include(if: $isVod) {{    value    signature    __typename  }}}}","variables":{{"isLive":{is_live},"login":"{channel}","isVod":{is_vod},"vodID":"{vod_number}","playerType":"site"}}}}'
TOKEN_API = 'https://gql.twitch.tv/gql'

LIVE_API = 'http://usher.twitch.tv/api/channel/hls/{channel}.m3u8?' +\
    '&token={token}&sig={sig}&allow_audio_only=true&allow_source=true'
# LIVE_TOKEN_API = 'http://api.twitch.tv/api/channels/{channel}/access_token?oauth_token={user_token}'

VOD_API = 'https://usher.ttvnw.net/vod/{vod_number}.m3u8?' +\
    '&token={token}&sig={sig}&allow_audio_only=true&allow_source=true'
# VOD_TOKEN_API = 'http://api.twitch.tv/api/vods/{vod_number}/access_token?oauth_token={user_token}'


def generate_token_query(channel, is_live, is_vod, vod_number=''):
    return TOKEN_QUERY.format(is_live=is_live, channel=channel, is_vod=is_vod, vod_number=vod_number)


def get_live_token_and_signature(channel, user_token):
    headers = {'Authorization': f'OAuth {user_token}'}
    token_query = generate_token_query(channel=channel, is_live='true', is_vod='false')
    response = requests.post(url=TOKEN_API, headers=headers, data=token_query).text
    data = json.loads(response)['data']['streamPlaybackAccessToken']
    sig = data['signature']
    token = data['value']
    return token, sig


def get_live_stream(channel, user_token):
    token, sig = get_live_token_and_signature(channel, user_token)
    url = LIVE_API.format(channel=channel, sig=sig, token=token)
    response = requests.get(url).text
    m3u8_obj = m3u8.loads(response)
    return m3u8_obj


def get_vod_token_and_signature(channel, vod_number, user_token):
    headers = {'Authorization': f'OAuth {user_token}'}
    token_query = generate_token_query(channel=channel, is_live='false', is_vod='true', vod_number=vod_number)
    response = requests.post(url=TOKEN_API, headers=headers, data=token_query).text
    print(response)
    data = json.loads(response)['data']['videoPlaybackAccessToken']
    sig = data['signature']
    token = data['value']
    return token, sig


def get_vod_stream(channel, vod_number, user_token):
    token, sig = get_vod_token_and_signature(channel, vod_number, user_token)
    url = VOD_API.format(vod_number=vod_number, token=token, sig=sig)
    response = requests.get(url).text
    m3u8_obj = m3u8.loads(response)
    return m3u8_obj


def download_mp3(uri, channel_name):
    current_date = datetime.today().strftime('%Y%m%d%H%M%S')
    (
        ffmpeg
        .input(uri)
        .output(f'{channel_name}_{current_date}.mp3')
        .global_args('-loglevel', 'info')
        .run()
    )


def download_mp4(uri, channel_name):
    current_date = datetime.today().strftime('%Y%m%d%H%M%S')
    (
        ffmpeg
        .input(uri)
        .output(f'{channel_name}_{current_date}.mp4')
        .global_args('-loglevel', 'info', '-c:v', 'nvenc_h264')
        .run()
    )


def get_video_urls(m3u8_obj):
    if m3u8_obj.playlists:
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
            if quality == "audio_only" or quality == "Audio Only":
                audio_uri = uri
            elif "source" in quality or 'chunked' in uri:
                source_uri = uri
        return source_uri, audio_uri
    else:
        print("No live video")
        exit()


def monitor_streaming(channel_name, user_token, file_type):
    while True:
        m3u8_obj = get_live_stream(channel_name, user_token)
        while not m3u8_obj.playlists:
            try:
                current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print(f'Wait for {channel_name} to start streaming, current time: {current_time}')
                time.sleep(600)
                m3u8_obj = get_live_stream(channel_name, user_token)
            except KeyboardInterrupt:
                print(f"exit monitor {channel_name}'s streaming")
                exit()
            except ConnectionError:
                print('Twitch API not stable, retry again')
                pass
        download_streaming(file_type, m3u8_obj, channel_name)


def download_streaming(file_type, m3u8_obj, channel_name):
    source_uri, audio_uri = get_video_urls(m3u8_obj)
    if file_type == 'mp3':
        download_mp3(audio_uri, channel_name)
    elif file_type == 'mp4':
        download_mp4(source_uri, channel_name)
    elif file_type != 'false':
        print('download argument only support "mp3" or "mp4"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('get video url of twitch channel')
    parser.add_argument('channel_name')
    parser.add_argument('--vod_number')
    parser.add_argument('user_token')
    parser.add_argument('download')
    args = parser.parse_args()
    if not args.vod_number:
        monitor_streaming(args.channel_name, args.user_token, args.download)
    else:
        m3u8_obj = get_vod_stream(args.channel_name, args.vod_number, args.user_token)
        download_streaming(args.download, m3u8_obj, args.channel_name)
