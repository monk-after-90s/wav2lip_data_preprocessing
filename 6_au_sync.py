import os
import sys
import numpy as np
import soundfile as sf
import librosa

dataset_path = sys.argv[1]
presenter_name = sys.argv[2]

obj_path = os.path.join(dataset_path, presenter_name)
ROOT = os.path.join(obj_path, "face_imgs")
print("ROOT:", ROOT)
start = 0
end = -1

with open(os.path.join(obj_path, f"filelist/raw_filelist.txt"), "r") as f:
    data = f.readlines()

data = [line.strip() for line in data]
data.sort()
data = data[start:]
print("Data", start, len(data), len(data))

errors = []
results = []
for p in data:
    try:
        frames = os.listdir(p)
        frames = [file for file in frames if ".jpg" in file]
        frame_count = len(frames)
        vid_duration = frame_count / 25
        # print(vid_duration)
        vid_name = p.split("/")[-1]

        org_path = os.path.join(p, f"{vid_name}.wav")
        au_path = os.path.join(p, "audio.wav")
        synced_path = os.path.join(p, "synced_audio.wav")

        if not os.path.isfile(au_path):
            status = os.system(f"ffmpeg -i {org_path} -ar 16000 {au_path}")
            if status != 0:
                errors.append(p)
                continue
        if not os.path.isfile(synced_path):
            au, sr = librosa.load(au_path, sr=16000)
            au_duration = au.shape[0] / sr

            extra = int(vid_duration * sr - au.shape[0])
            is_append = extra >= 0
            extra = abs(extra)
            new_au = au
            if extra > 0:
                front = False
                if (is_append):
                    # append audio
                    if front:
                        new_au = np.concatenate([np.zeros(extra), au])
                    else:
                        new_au = np.concatenate([au, np.zeros(extra)])
                else:
                    # cut audio
                    if front:
                        new_au = au[:-extra]
                    else:
                        new_au = au[extra:]
            sf.write(synced_path, new_au, sr)
        results.append(p)
    except Exception:
        print(p)
        errors.append(p)
if not os.path.exists(os.path.join(obj_path, f"filelist/temp")):
    os.mkdir(os.path.join(obj_path, f"filelist/temp"))

with open(os.path.join(obj_path, f"filelist/temp/output_synced_{start}_{len(data)}.txt"), "w") as f:
    for line in results:
        f.write(line + "\n")

with open(os.path.join(obj_path, f"filelist/temp/output_synced_errors_{start}_{len(data)}.txt"), "w") as f:
    for line in errors:
        f.write(line + "\n")
