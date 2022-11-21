import pyaudio
import wave
import keyboard
import sys
import os
import re

if __name__ == "__main__":
    if len(sys.argv[1]) > 0:
        label = sys.argv[1]

        CHUNK = 1600
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        seconds = 5
        training_data_path = 'C:/Users/dnlrm/jenna-training-data'
        recs_path = f"{training_data_path}/{label}"
        os.chdir(training_data_path)
        if not os.path.isdir(label):
            os.mkdir(label)
        os.chdir(label)
        dirs = os.listdir()
        suffix = 0
        print("Initial suffix: " + str(suffix))
        if len(dirs) > 0:
            # Files sort by date created
            dirs.sort(key=os.path.getctime)
            # Get latest and extract actual suffix if any
            latest_file = dirs[len(dirs)-1]
            try:
                match = re.search('^'+label+'([0-9]*).wav$', latest_file)
                if match:
                    suffix = int(match.group(1))
                    suffix += 1
                    print(f"Suffix set to {suffix}")
            except Exception:
                pass

        while True:
            try:
                key = input(f"Rec#{suffix}: Press [Enter] to record, [q+Enter] to quit: ")
                if key == "":
                    while True:
                        data = stream.read(CHUNK)
                        frames.append(data)

                        if keyboard.is_pressed("escape"):
                            print(f"#{suffix} terminated. Writing wav...")
                            wf = wave.open(f"{recs_path}/{label}{suffix}.wav", 'wb')
                            wf.setnchannels(CHANNELS)
                            wf.setsampwidth(p.get_sample_size(FORMAT))
                            wf.setframerate(RATE)
                            wf.writeframes(b''.join(frames))
                            wf.close()
                            frames = []
                            suffix += 1
                            break

                elif key == "q" or key == "Q":
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    break
            except KeyboardInterrupt:
                stream.stop_stream()
                stream.close()
                p.terminate()