import pyaudio
import sys
import wave
import os
import re

if __name__ == "__main__":
    CHUNK = 1600
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    training_data_path = 'C:/Users/dnlrm/jenna-training-data'
    os.chdir(training_data_path)
    background_audio_data_dir = 'background-audio'
    recs_path = training_data_path + '/' + background_audio_data_dir
    if not os.path.isdir(background_audio_data_dir):
        os.mkdir(background_audio_data_dir)
    os.chdir(background_audio_data_dir)
    dirs = os.listdir()
    suffix = 0
    print("Initial suffix: " + str(suffix))
    if len(dirs) > 0:
        # Files sort by date created
        dirs.sort(key=os.path.getctime)
        # Get latest and extract actual suffix if any
        latest_file = dirs[len(dirs)-1]
        try:
            match = re.search('^background([0-9]*).wav$', latest_file)
            if match:
                suffix = int(match.group(1))
                suffix += 1
                print(f"Suffix set to {suffix}")
        except Exception:
            pass

    p = pyaudio.PyAudio()
    stream = p.open(rate=RATE,
                    channels=CHANNELS,
                    format=FORMAT,
                    input=True,
                    frames_per_buffer=CHUNK)

    seconds = 10
    try:
        seconds = int(sys.argv[1])
    except Exception:
        pass
    target_num_buffers = seconds * RATE / CHUNK
    num_buffers_per_file = 10 * RATE / CHUNK
    total_buffers = 0

    frames = []
    print(f"Collection background audio... {seconds} seconds, {target_num_buffers} target # buffers")

    while total_buffers < target_num_buffers:
        data = stream.read(CHUNK)
        frames.append(data)
        total_buffers += 1
        if len(frames) == num_buffers_per_file:
            # Save file
            wf = wave.open(f"{recs_path}/background{suffix}.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            frames = []
            suffix += 1
            print(f"Total buffers collected: {total_buffers}")
        