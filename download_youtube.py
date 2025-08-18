from __future__ import unicode_literals
import yt_dlp as youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("下載完成，正在轉換格式")
    elif d["status"] == "downloading":
        print(
            f"下載中，下載檔名：{d.get('info_dict').get('title')}，已下載 {d.get('downloaded_bytes')/1024/1024:.2f} / {d.get('total_bytes')/1024/1024:.2f} MB"
        )


ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "youtube_music/%(title)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
    "ffmpeg_location": "ffmpeg/bin/ffmpeg.exe",
}
if __name__ == "__main__":
    while True:
        try:
            youtube_id = input("請輸入youtube網址，如果要結束請按Ctrl+C：\n")
            if "=" in youtube_id:
                youtube_id = youtube_id.split("=")[1]
            if "&" in youtube_id:
                youtube_id = youtube_id.split("&")[0]
            print("開始下載")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(["https://www.youtube.com/watch?v=%s" % youtube_id])
        except KeyboardInterrupt:
            print(f"結束下載")
            exit()
        except Exception as e:
            print(f"有東西出錯了：{e}")
