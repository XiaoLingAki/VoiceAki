import requests
import wave
import pygame
from io import BytesIO

def play_text_to_speech(text, path, format = "wav", id = 226, length = 1.3):
    # 构建API请求URL
    api_url = f"http://123.207.0.178:23456/voice/vits?text={text}&id={id}&format={format}&length={length}"

    try:
        # 发送HTTP GET请求获取音频文件
        response = requests.get(api_url)
        response.raise_for_status()  # 检查是否有错误发生

        # 保存音频文件到本地
        with open(path, "wb") as file:
            file.write(response.content)

        # 使用pygame播放音频文件
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        # 等待音频播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

# # 示例调用
# text = "晚上好，今天也是开心的一天呢"
# format = "wav"
# id = 226
# length = 1.3

# success = play_text_to_speech(text, format, id, length)
# if success:
#     print("音频播放成功")
# else:
#     print("音频播放失败")
