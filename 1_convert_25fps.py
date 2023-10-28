import os
import concurrent.futures
import subprocess
import sys

input_video_path = sys.argv[1]
output_video_path = sys.argv[2]
n_processes = int(sys.argv[3])

if not os.path.exists(output_video_path):
    os.makedirs(output_video_path)
source_dir = os.listdir(input_video_path)


def convert_25fps(name_video):
    video = os.path.join(input_video_path, name_video)
    new_video = os.path.join(output_video_path, name_video)
    subprocess.call(f"ffmpeg -y -i {video} -filter:v fps=25 -b:v 50M {new_video}", shell=True)


with concurrent.futures.ProcessPoolExecutor(n_processes) as executor:
    inputs = [x for x in source_dir]
    executor.map(convert_25fps, inputs)
