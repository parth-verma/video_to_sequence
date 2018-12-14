#-*- coding: utf-8 -*-
import subprocess
from pytube import YouTube
from youtube_dl import YoutubeDL
import pandas as pd
import numpy as np
import skvideo.io
import cv2
import os


def download_and_process_video(save_path, row):
    video_id = row['VideoID']
    video_path = row['video_path']
    full_path = os.path.join(save_path, video_path)
    if os.path.exists( full_path ):
        return

    start = row['Start']
    end = row['End']

    print("Downloading", "http://youtube.com/watch?v="+video_id)

    if os.path.exists('tmp.mp4'):
        os.system('rm -f tmp.*')
    subprocess.run("youtube-dl \'https://www.youtube.com/watch?v="+video_id+"' -f \'best[height=360]\' --output 'videos/%(id)s.%(ext)s'",stdout=subprocess.PIPE)
    return
#    try: # 다운로드 포기
 #       youtube = YouTube("http://youtube.com/watch?v="+video_id).stream.filter(subtype='mp4',res='360p').first().download(filename="tmp.mp4")
  #  except Exception as e:
   #     print(e)
    #    return
 #ydl_opts = {'outtmpl': 'tmp.%(ext)s','format': 'best[height=360]','postprocessors': [{
  #      'key': 'FFmpegVideoConvertor',
   #     'preferedformat': 'mp4',  # one of avi, flv, mkv,mp4, ogg, webm
#        '--strict':'2'
   # }]}
    #with YoutubeDL(ydl_opts) as ydl:
     #   ydl.download(["http://youtube.com/watch?v="+video_id])

    cap = cv2.VideoCapture( 'tmp.mp4' )
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = int(cap.get(cv2.FOURCC(*'XVID')))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter( full_path, fourcc, fps, (w,h))

    start_frame = int(fps * start)
    end_frame = int(fps * end)

    frame_count = 0
    while frame_count < end_frame:
        ret, frame = cap.read()
        frame_count += 1

        if frame_count >= start_frame:
            out.write(frame)

    cap.release()
    out.release()

def main():
    video_data_path='./final.csv'
    video_save_path = './data/youtube_videos'

    video_data = pd.read_csv(video_data_path, sep=',')
    video_data = video_data[video_data['Language'] == 'English']
    video_data['video_path'] = video_data.apply(lambda row: row['VideoID']+'_'+str(row['Start'])+'_'+str(row['End'])+'.avi', axis=1)

    video_data.apply(lambda row: download_and_process_video(video_save_path, row), axis=1)

if __name__=="__main__":
    main()
