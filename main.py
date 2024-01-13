import pyaudio
import numpy as np
import wave
import time
import utils
import gpt
import json
import loguru
import os
from vits import play_text_to_speech

p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


def record():
    while True:
        RECORDING = False
        TS = 0
        T0 = 0  #开始录音的时间点
        T1 = 0
        frames = []

        try:
            while True:
                # print(frames)
                data = stream.read(CHUNK)
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.max(audio_data)
                print(f"当前音量: {volume}")

                if volume > 2000 and not RECORDING:
                    T0 = time.time()
                    T1 = time.time()
                    RECORDING = True
                    frames = frames[-5:]

                if RECORDING:
                    frames.append(data)

                if volume < 2000 and RECORDING:
                    if time.time() - T0 > 1:
                        T1 = time.time()
                        RECORDING = False

                        # 保存录制的音频
                        wf = wave.open("audio.wav", 'wb')
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()

                        print("录音保存成功.")
                        
                        request = utils.speech2text(utils.get_file_content_as_base64("./audio.wav"))
                        # print(request)
                        response_dict = json.loads(request)
                        awake = response_dict.get('result', [])
                        print(awake[0])
                        keywords = ["粉", "嗯", "毛", "猫","分","么"]
    
                        recognize = False
                        for keyword in keywords:
                            if keyword in awake[0]:
                                print("唤醒词匹配成功")
                                recognize = True

                        # 尝试识别唤醒词
                        if recognize:
                            print("开始对话处理。")
                            play_text_to_speech("嗨","./awake.wav")
                            # os.remove("./result.wav")
                            process()
                            # 在这里可以开始对话处理流程
                            break
                        else:
                            print("未匹配到唤醒词，继续监听。")

        except KeyboardInterrupt:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()


def process():
    f = True
    while f:
        f = False
        RECORDING = False
        T0 = 0
        T1 = 0
        frames = []

        try:
            while True:
                data = stream.read(CHUNK)
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.max(audio_data)
                print(f"当前音量: {volume}")

                if volume > 2000 and not RECORDING:
                    T0 = time.time()
                    RECORDING = True
                    frames = frames[-5:]

                if RECORDING:
                    frames.append(data)

                if volume < 1000 and RECORDING:
                    if time.time() - T0 > 2:
                        T1 = time.time()
                        RECORDING = False

                        # 保存录制的音频
                        wf = wave.open("speech.wav", 'wb')
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()

                        print("录音保存成功.")
                        
                        request = utils.speech2text(utils.get_file_content_as_base64("./speech.wav"))
                        # print(request)
                        response_dict = json.loads(request)
                        speech = response_dict.get('result', [])
                        
                        loguru.logger.debug(speech[0])
                        result = utils.response_generate(prompt='#粉毛 ' + speech[0])
                        
                        loguru.logger.debug(result)
                        play_text_to_speech(result,"./response.wav")
                        return

        except KeyboardInterrupt:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    
if __name__ == "__main__":
    record()
