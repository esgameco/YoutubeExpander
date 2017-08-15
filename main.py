import pafy
from moviepy.editor import *
import os
import sys

# Get video from youtube
video_url = input("Enter Video URL: ")
video = pafy.new(video_url)

# Get maximum
MAXIMUM = int(input("Enter The Max Number Present: "))


def show_resolution(resolutions):
    for res in range(len(resolutions)):
        height = resolutions[res][0]
        width = resolutions[res][1]
        print(str(res+1) + ". (" + str(width) + "/" + str(height) + ")")

# Get resolution
if input("Would you like to use a default resolution? (Y/N)") == 'y':
    NORMAL_RESOLUTIONS = ((640, 480), (960, 720), (768, 1024), (1200, 1920), (1600, 2560))
    WIDESCREEN_RESOLUTIONS = ((1280, 720), (1366, 768), (1600, 900), (1920, 1080), (2560, 1440), (3840, 2160))
    if input("Do you want to use a widescreen (1) or a normal resolution (2)? ") == 1:
        show_resolution(WIDESCREEN_RESOLUTIONS)
        RESOLUTION = WIDESCREEN_RESOLUTIONS[int(input("Which would you like to use? "))-1]
    else:
        show_resolution(NORMAL_RESOLUTIONS)
        RESOLUTION = NORMAL_RESOLUTIONS[int(input("Which would you like to use? "))-1]
else:
    HEIGHT = int(input("Enter The Height: "))
    WIDTH = int(input("Enter The Width: "))
    RESOLUTION = (HEIGHT, WIDTH)

HEIGHT = RESOLUTION[0]
WIDTH = RESOLUTION[1]
FOURTH_RESOLUTION = (int(HEIGHT/2), int(WIDTH/2))

path = "/Expander/" + video.videoid
output_path = path + "/Output/"
videos_path = path + "/Videos/"
if not os.path.exists(path):
    os.makedirs(output_path)
    os.makedirs(videos_path)
    os.rename(video.getbest('mp4').download(videos_path), videos_path + "1.mp4")
else:
    sys.exit(100) # Error if path exists

output_videos = list()
output_videos.append(VideoFileClip(filename=videos_path + "1.mp4", target_resolution=RESOLUTION))


def standard():
    current_total = 1
    while current_total < MAXIMUM:
        current_path = videos_path + str(current_total) + ".mp4"
        video_clip = VideoFileClip(filename=current_path, target_resolution=FOURTH_RESOLUTION)
        four_times_clip = CompositeVideoClip(clips=[video_clip.set_position((0, 0)),
                                                    video_clip.set_position((WIDTH/2, 0)),
                                                    video_clip.set_position((0, HEIGHT/2)),
                                                    video_clip.set_position((WIDTH/2, HEIGHT/2))], size=(WIDTH, HEIGHT))
        four_times_clip.write_videofile(videos_path + str(current_total * 4) + ".mp4")
        output_videos.append(four_times_clip)
        current_total *= 4


def delayed():
    current_total = 1
    while current_total < MAXIMUM:
        current_path = videos_path + str(current_total) + ".mp4"
        video_clip = VideoFileClip(filename=current_path, target_resolution=FOURTH_RESOLUTION)
        four_times_clip = CompositeVideoClip(clips=[video_clip.set_position((0, 0)),
                                                    video_clip.set_position((WIDTH / 2, 0)).set_start(0.05),
                                                    video_clip.set_position((0, HEIGHT / 2)).set_start(0.05),
                                                    video_clip.set_position((WIDTH / 2, HEIGHT / 2)).set_start(0.10)],
                                             size=(WIDTH, HEIGHT))
        four_times_clip.write_videofile(videos_path + str(current_total * 4) + ".mp4")
        output_videos.append(four_times_clip)
        current_total *= 4

choice = input("Which would you like to do?\n"
               "1. Standard - No Delay, Fast\n"
               "2. Delayed - Delay, Very Slow\n"
               "Enter: ")
if int(choice) is 1:
    standard()
else:
    delayed()

output_file = concatenate_videoclips(output_videos)
output_file.write_videofile(output_path + "output.mp4")
