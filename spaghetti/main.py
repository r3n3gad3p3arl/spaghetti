import os
import shutil
import random
import math
import ffmpeg
import config
from clip import Clip

clips = []
        
# Get a random number of clips from 'sources' directory.
for root, dirs, files in os.walk("sources"):
    for file in files:
        clips.append(Clip(os.path.join(root, file)))

source_clip_num = min(random.randint(config.min_source_clip_num, config.max_source_clip_num), len(clips))
clips = random.sample(clips, k=source_clip_num)

# Cut a random number of subclips from each source clip.
if os.path.isdir("temp"):
    shutil.rmtree("temp")

os.mkdir("temp")

subclips = []

for i, clip in enumerate(clips):
    for x in range(random.randint(config.min_subclip_num, config.max_subclip_num)):
        subclip_length = min(random.uniform(config.min_subclip_length, config.max_subclip_length), clip.duration)
        subclip_start = random.uniform(0, clip.duration - subclip_length)

        subclip_video = clip.video.trim(start=subclip_start, duration=subclip_length).setpts("PTS-STARTPTS")
        subclip_audio = clip.audio.filter("atrim", start=subclip_start, duration=subclip_length).filter("asetpts", "PTS-STARTPTS")
        subclip_output_name = f"temp/subclip{i}_{x}.mp4"
        
        ffmpeg.output(subclip_video, subclip_audio, subclip_output_name).run()
        subclips.append(Clip(subclip_output_name))
        
clips = subclips
            
# Resize all subclips to a consistent size.
clips.sort(reverse=True, key=lambda clip : clip.dimensions[1])

clip_0_width, clip_0_height = clips[0].dimensions

for i, clip in enumerate(clips):
    clip.resize(clip_0_width, clip_0_height)

# Apply random effects to subclips.
for i, clip in enumerate(clips):
    effects_num = min(random.randint(config.min_effects, config.max_effects), len(config.effects))
    subclip_effects = random.sample(config.effects, k=effects_num)
    
    for effect in subclip_effects:
        f_effect = getattr(clip, effect)

        if effect == "speedx":
            speedx_factor = random.uniform(config.min_speedx_factor, config.max_speedx_factor)
            speed = random.choice(["slow", "fast"])
            
            # Due to limits with FFmpeg, slowed clips are clamped at 0.5 speed.
            # I might come up with a better solution later.
            if speed == "slow":
                speedx_factor = max(1 / speedx_factor, 0.5)

            f_effect(speedx_factor)

        elif effect == "vibrato":
            f_effect(config.vibrato_freq)
                
        else:
            f_effect()
            
# Concatenate all subclips and output resulting video.
def generate_video_name(name):
    video_id = 0

    while os.path.exists(f"output/{name}{video_id}.mp4"):
        video_id += 1
        
    return f"output/{name}{video_id}.mp4"
        
random.shuffle(clips)

video_output = []
for clip in clips:
    video_output.append(clip.video)
    video_output.append(clip.audio)

if not os.path.isdir("output"):
    os.mkdir("output")

ffmpeg.output(ffmpeg.concat(*video_output, v=1, a=1, unsafe=1), generate_video_name("ytp"), fpsmax=60).run()

shutil.rmtree("temp")
