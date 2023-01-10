import os
import shutil
import subprocess

recording_folder = "./行車記錄器"

def collect_recording_by_day():
    recording_list = os.listdir(recording_folder)
    for recording_file in recording_list:
        if ".mp4" not in recording_file and ".MP4" not in recording_file:
            print(f"{recording_file} is not a recording file, skip this item")
            continue
        day = recording_file.split('-')[0][-8:len(recording_file)]
        day_folder = f"{recording_folder}/{day}"
        if not os.path.exists(day_folder):
            os.makedirs(day_folder)
        shutil.move(f"{recording_folder}/{recording_file}", f"{day_folder}/{recording_file}")

def rotate_and_aggregate_recording():
    folder_list = os.listdir(recording_folder)
    for folder in folder_list:
        recording_list = os.listdir(f"{recording_folder}/{folder}")
        file_prefix = f"{recording_folder}/{folder}/{folder}"
        if os.path.exists(f"{file_prefix}.mp4"):
            print("already has aggregate file in {folder} folder, skip this folder")
            continue
        with open(f"{file_prefix}.txt", 'a', encoding='UTF-8') as concat_file:
            for recording_file in recording_list:
                concat_file.write(f"file {recording_file}\n")
            print("prepared file list txt for ffmpeg input")
        print(f"start to process {file_prefix}.mp4")
        subprocess.run(f"ffmpeg -loglevel error -safe 0 -f concat -i {file_prefix}.txt -vf \"hflip,vflip\" {file_prefix}.mp4")
            

if __name__ == "__main__":
    collect_recording_by_day()
    rotate_and_aggregate_recording()