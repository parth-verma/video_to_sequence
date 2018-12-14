import csv
import glob
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

CSV_PATH = "withoutrepeat.csv"
VIDEOS_DIR_PATH = "videos/"
reader = csv.reader(open(CSV_PATH, "r"), delimiter=',')
for line in reader:
    x = glob.glob(VIDEOS_DIR_PATH + ','.join(line[:1]) + ".*")
    if len(x) == 1:
        start_time = int(''.join(line[1:2]))
        end_time = int(''.join(line[2:3]))

        CURRENT_VIDEO_PATH = x[0]

        DIST_PATH = 'clipped_videos/' + ','.join(line[:1]) + '_' + str(start_time) + '_' + str(end_time) + ".avi"
        ffmpeg_extract_subclip(CURRENT_VIDEO_PATH, start_time, end_time, DIST_PATH)
        os.remove(CURRENT_VIDEO_PATH)
