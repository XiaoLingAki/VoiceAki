import json
import requests
import wave
import urllib
import base64
import os

API_KEY = "***"
SECRET_KEY = "***"

def get_audio_file_size(file_path = './audio.wav'):
    try:
        # 获取文件大小（字节数）
        size_in_bytes = os.path.getsize(file_path)
        print(size_in_bytes)
        return size_in_bytes
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到.")
        return None

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_file_content_as_base64(path = './audio.wav', urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
        
    length = get_audio_file_size(path)
    return content, length

def speech2text(audio_file):
        
    url = "https://vop.baidu.com/server_api"
    
    speech, length = audio_file
    payload = json.dumps({
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": "zj1pNbVnq5Q5NW9W4dV4ns6fsWME6OXI",
        "speech":speech,
        "len": length,
        "token": get_access_token()
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text
    
    
def response_generate(prompt, history = []):
    url = "http://123.207.0.178:8000"
    data = {
        "prompt": prompt,
        "history": history
    }
    response_json = requests.post(url, json=data).json()
    
    return response_json["response"]
    
if __name__ == "__main__":
    speech2text(get_file_content_as_base64())
